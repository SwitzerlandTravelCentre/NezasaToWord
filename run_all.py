"""
run_all.py

High-level orchestrator:

1. Fetch booking JSON from Nezasa (nezasa_fetch_booking.py logic)
2. Generate Word document from the JSON and booking_template.docx

You can show this to IT as the main entry point.
"""

from pathlib import Path
import json
import os

from docx import Document  # ensures dependency is visible in this script
import requests

# --- Config -------------------------------------------------------------------

BASE_URL = "https://api.nezasa.com"  # adapt
BOOKING_ID = "ucq6nmw9fx7a"
API_KEY = os.getenv("NEZASA_API_KEY")
JSON_PATH = Path("nezasa_booking.json")
TEMPLATE_PATH = Path("booking_template.docx")
OUTPUT_DIR = Path("output_docs")
OUTPUT_DIR.mkdir(exist_ok=True)


# --- Minimal versions of helpers from other scripts ---------------------------

def fetch_booking(booking_id: str) -> dict:
    if not API_KEY:
        raise RuntimeError("NEZASA_API_KEY not set in environment.")

    url = f"{BASE_URL}/bookings/{booking_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    # Step 1: fetch booking
    print(f"Fetching booking {BOOKING_ID}…")
    data = fetch_booking(BOOKING_ID)
    save_json(data, JSON_PATH)
    print(f"Saved JSON to {JSON_PATH.resolve()}")

    # Step 2: generate Word document by calling generate_booking_doc.py logic
    # Instead of importing, we can just run the other script via command line,
    # or you can import generate_booking_doc and call generate_word_from_json().
    try:
        from generate_booking_doc import generate_word_from_json  # type: ignore
    except ImportError:
        print(
            "Could not import generate_booking_doc. "
            "Make sure generate_booking_doc.py is in the same folder."
        )
        return

    output_path = generate_word_from_json(TEMPLATE_PATH, JSON_PATH, OUTPUT_DIR)
    print(f"Generated Word document: {output_path.resolve()}")


if __name__ == "__main__":
    main()
