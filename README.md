# NezasaToWord

NezasaToWord is a small Python tool for travel agencies using Nezasa /
TripBuilder. It provides a simple desktop interface where users can enter a
Booking ID and their Booking API credentials, download the complete raw booking
data, and save it locally as a JSON file.

The downloaded JSON can then be reviewed, archived, or used as input for later
workflows such as reporting, automation, or document generation.

Current scope:

```text
Booking ID + Distribution Channel + Booking API username/password
  -> Nezasa Booking API
  -> booking_<booking_id>.json
```

JSON-to-Word generation is currently on hold and intentionally not part of the
active codebase.

## Active Files

```text
app/nezasa_fetch_ui.py          Tkinter GUI for fetching and saving booking JSON
requirements.txt                Python runtime dependencies
docs/TECHNICAL_SPECIFICATION.md Detailed technical specification
SECURITY.md                    Public-repository security and data-handling rules
.gitignore                      Excludes credentials, JSON data, and generated documents
.gitattributes                  Line-ending normalization
```

## Requirements

- Python 3
- `requests`
- Tkinter, usually included with standard Python installations on Windows

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Run

```powershell
py app\nezasa_fetch_ui.py
```

The application asks for:

- Distribution Channel
- Booking API username
- Booking ID
- Booking API password

The username and distribution channel can optionally be prefilled with
environment variables:

```text
NEZASA_API_USERNAME
NEZASA_DISTRIBUTION_CHANNEL
```

Credentials must never be committed to GitHub.

## Output

On success, the application saves the raw API response as:

```text
booking_<booking_id>.json
```

The file is saved to the detected Desktop location. If no Desktop path can be
found, the user home directory is used as a fallback.

Generated JSON files can contain customer and booking data and are ignored by
Git.

Because this repository is public, read [SECURITY.md](SECURITY.md) before
adding sample data, screenshots, issues, or documentation.

## API Contract

```text
GET https://{distribution-channel}.tripbuilder.app/bookings/v1.13/{booking_id}
Accept: application/vnd.api+json
Authentication: HTTP Basic Auth
```

See [docs/TECHNICAL_SPECIFICATION.md](docs/TECHNICAL_SPECIFICATION.md) for
detailed implementation notes and troubleshooting.
