"""
nezasa_fetch_booking.py

- Fetches a booking from Nezasa API
- Saves the JSON to a local file: nezasa_booking.json

Dependencies:
    pip install requests
"""

import os
import json
from pathlib import Path

import requests

# === CONFIGURATION (adapt to your environment) ================================

# Example base URL – adapt to your Nezasa environment
BASE_URL = "https://api.nezasa.com"  # <-- CHANGE if your endpoint differs

# The booking ID you want to fetch (example from your JSON)
BOOKING_ID = "gxys6fk8bjpj"  # <-- can be parameterised later

# Where to save the JSON
OUTPUT_JSON_PATH = Path("nezasa_booking.json")

# API key/token – IT will probably want this in an environment variable
# Example: set NEZASA_API_KEY in system/user environment
API_KEY = os.getenv("NEZASA_API_KEY")  # <-- set this in your environment


def fetch_booking(booking_id: str) -> dict:
    """
    Call the Nezasa API to fetch booking details.
    The exact endpoint and auth scheme may differ; adapt as needed.
    """
    if not API_KEY:
        raise RuntimeError(
            "Missing NEZASA_API_KEY environment variable. "
            "Please configure it before running this script."
        )

    # Example endpoint – adjust to the real Nezasa booking endpoint
    url = f"{BASE_URL}/bookings/{booking_id}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    print(f"Fetching booking {BOOKING_ID} from Nezasa…")
    data = fetch_booking(BOOKING_ID)

    with OUTPUT_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved booking JSON to: {OUTPUT_JSON_PATH.resolve()}")


if __name__ == "__main__":
    main()
