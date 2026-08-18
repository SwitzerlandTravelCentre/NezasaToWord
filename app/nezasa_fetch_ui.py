"""
Nezasa Booking JSON Fetcher.

Small GUI for travel agencies using Nezasa / TripBuilder:
enter a Booking ID, fetch the confirmed booking via the Booking API, and save
the complete raw JSON response locally.

JSON-to-Word generation is intentionally out of scope for this file.
"""

from __future__ import annotations

import tkinter as tk
import json
import os
import re
from pathlib import Path
from tkinter import messagebox
from typing import Any


DEFAULT_API_USERNAME = os.environ.get("NEZASA_API_USERNAME", "")
DEFAULT_DISTRIBUTION_CHANNEL = os.environ.get("NEZASA_DISTRIBUTION_CHANNEL", "")
BOOKING_API_VERSION = "v1.13"
ACCEPT_HEADER = "application/vnd.api+json"
REQUEST_TIMEOUT_SECONDS = 30


def load_requests_modules():
    try:
        import requests
        from requests.auth import HTTPBasicAuth
    except ImportError as exc:
        raise RuntimeError(
            "Missing Python dependency 'requests'. Install it with:\n\n"
            "py -m pip install -r requirements.txt"
        ) from exc

    return requests, HTTPBasicAuth


def get_default_output_dir() -> Path:
    """
    Return a useful save location in Windows/OneDrive environments.
    """
    userprofile = Path(os.environ.get("USERPROFILE", str(Path.home())))
    candidates = [
        userprofile / "Desktop",
        userprofile / "OneDrive" / "Desktop",
    ]

    onedrive = os.environ.get("OneDrive")
    if onedrive:
        candidates.append(Path(onedrive) / "Desktop")

    for path in candidates:
        if path.exists() and path.is_dir():
            return path

    return Path.home()


def sanitize_booking_id(raw_booking_id: str) -> str:
    """
    Clean pasted Booking IDs before using them in URLs or filenames.
    """
    booking_id = raw_booking_id.strip()
    booking_id = re.sub(r"\s+", "", booking_id)
    booking_id = booking_id.lower()
    booking_id = re.sub(r"[^a-z0-9_-]", "", booking_id)
    return booking_id


def sanitize_distribution_channel(raw_channel: str) -> str:
    channel = raw_channel.strip().lower()
    channel = re.sub(r"[^a-z0-9-]", "", channel)
    return channel


def build_booking_url(distribution_channel: str, booking_id: str) -> str:
    return (
        f"https://{distribution_channel}.tripbuilder.app/"
        f"bookings/{BOOKING_API_VERSION}/{booking_id}"
    )


def build_output_path(booking_id: str) -> Path:
    return get_default_output_dir() / f"booking_{booking_id}.json"


def fetch_booking_json(
    distribution_channel: str,
    booking_id: str,
    username: str,
    password: str,
) -> dict[str, Any]:
    requests, HTTPBasicAuth = load_requests_modules()
    url = build_booking_url(distribution_channel, booking_id)
    headers = {"Accept": ACCEPT_HEADER}

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, password),
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            "The Booking API request failed before a response was received.\n\n"
            f"{exc}"
        ) from exc

    if response.status_code == 401:
        raise RuntimeError(
            "HTTP 401 Unauthorized.\n\n"
            "Check the Booking API password and confirm that the API user has "
            "the BookingAPI role."
        )

    if response.status_code == 404:
        raise RuntimeError(
            "HTTP 404 Not Found.\n\n"
            "Check the Booking ID and Distribution Channel.\n\n"
            f"URL used:\n{url}"
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP {response.status_code}\n\n"
            f"{response.text[:800]}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise RuntimeError(
            "The Booking API response was not valid JSON.\n\n"
            f"{response.text[:800]}"
        ) from exc


def save_booking_json(booking_json: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(booking_json, file, ensure_ascii=False, indent=2)
        file.write("\n")


def fetch_and_save(
    distribution_channel: str,
    booking_id: str,
    username: str,
    password: str,
) -> Path:
    booking_json = fetch_booking_json(
        distribution_channel=distribution_channel,
        booking_id=booking_id,
        username=username,
        password=password,
    )
    output_path = build_output_path(booking_id)
    save_booking_json(booking_json, output_path)
    return output_path


class NezasaFetchApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Nezasa Booking JSON Fetcher")
        self.root.geometry("480x330")
        self.root.resizable(False, False)

        tk.Label(root, text="Distribution Channel:").pack(pady=(15, 0))
        self.channel_entry = tk.Entry(root, width=40)
        if DEFAULT_DISTRIBUTION_CHANNEL:
            self.channel_entry.insert(0, DEFAULT_DISTRIBUTION_CHANNEL)
        self.channel_entry.pack()

        tk.Label(root, text="API Username:").pack(pady=(10, 0))
        self.username_entry = tk.Entry(root, width=40)
        self.username_entry.insert(0, DEFAULT_API_USERNAME)
        self.username_entry.pack()

        tk.Label(root, text="Booking ID:").pack(pady=(10, 0))
        self.booking_entry = tk.Entry(root, width=40)
        self.booking_entry.pack()

        tk.Label(root, text="API Key / Password:").pack(pady=(10, 0))
        self.password_entry = tk.Entry(root, width=40, show="*")
        self.password_entry.pack()

        tk.Button(
            root,
            text="Fetch & Save JSON",
            command=self.on_fetch,
            width=22,
            height=2,
        ).pack(pady=22)

    def on_fetch(self) -> None:
        distribution_channel = sanitize_distribution_channel(self.channel_entry.get())
        username = self.username_entry.get().strip()
        booking_id = sanitize_booking_id(self.booking_entry.get())
        password = self.password_entry.get().strip()

        if not distribution_channel:
            messagebox.showerror("Error", "Please enter the Distribution Channel.")
            return

        if not username:
            messagebox.showerror("Error", "Please enter the API username.")
            return

        if not booking_id:
            messagebox.showerror("Error", "Please enter a Booking ID.")
            return

        if not password:
            messagebox.showerror("Error", "Please enter the API key/password.")
            return

        try:
            output_path = fetch_and_save(
                distribution_channel=distribution_channel,
                booking_id=booking_id,
                username=username,
                password=password,
            )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        messagebox.showinfo("Success", f"Booking JSON saved:\n\n{output_path}")


def main() -> None:
    root = tk.Tk()
    NezasaFetchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
