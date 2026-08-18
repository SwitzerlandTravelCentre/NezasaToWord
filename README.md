# NezasaToWord

Internal STC prototype for fetching raw Nezasa / TripBuilder booking JSON files.

Current scope:

```text
Booking ID + Distribution Channel + Booking API username/password
  -> Nezasa Booking API
  -> booking_<booking_id>.json
```

JSON-to-Word generation is on hold and is intentionally not part of the active
codebase.

## Active Files

```text
app/nezasa_fetch_ui.py          Tkinter GUI for fetching and saving booking JSON
requirements.txt                Runtime Python dependencies
docs/TECHNICAL_SPECIFICATION.md Detailed API and implementation specification
SECURITY.md                    Public-repo security and data-handling rules
.gitignore                      Excludes credentials, raw JSON, and generated docs
.gitattributes                  Line-ending normalization
```

## Requirements

- Python 3
- `requests`
- Tkinter, included with standard Windows Python installations

Install dependencies:

```powershell
py -m pip install -r requirements.txt
```

## Run

```powershell
py app\nezasa_fetch_ui.py
```

The GUI asks for:

- Distribution Channel, default `stc-ch`
- Booking API username
- Booking ID
- Booking API password

The username can optionally be prefilled with the `NEZASA_API_USERNAME`
environment variable. Credentials must never be committed to GitHub.

## Output

On success, the GUI saves the raw API response as:

```text
booking_<booking_id>.json
```

The file is saved to the detected Desktop location. If no Desktop path can be
found, it falls back to the user home directory.

Generated JSON files contain customer and booking data and are ignored by Git.

Because this repository is public, see [SECURITY.md](SECURITY.md) before adding
sample data, screenshots, issues, or documentation.

## Known-Good API Contract

```text
GET https://{distribution-channel}.tripbuilder.app/bookings/v1.13/{booking_id}
Accept: application/vnd.api+json
Authentication: HTTP Basic Auth
```

Known-good default:

```text
Distribution Channel: stc-ch
```

See [docs/TECHNICAL_SPECIFICATION.md](docs/TECHNICAL_SPECIFICATION.md) for
detailed implementation notes and troubleshooting.
