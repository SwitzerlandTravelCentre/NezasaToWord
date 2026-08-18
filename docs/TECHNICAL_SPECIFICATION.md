# Technical Specification

## 1. Purpose

This repository contains the current Step 1 prototype for travel agencies using
Nezasa / TripBuilder: fetch confirmed booking data by Booking ID and save the
raw JSON response locally.

The long-term project may later generate editable Word travel documents, but
that phase is explicitly on hold.

## 2. Active Scope

The active workflow is:

```text
Travel agency user
  -> enters Distribution Channel
  -> enters API Username
  -> enters Booking ID
  -> enters Booking API password
  -> clicks Fetch & Save JSON
  -> receives booking_<booking_id>.json
```

Only `app/nezasa_fetch_ui.py` implements this active workflow.

## 3. Non-Scope

The following are not part of the current implementation:

- JSON normalization into an internal travel model
- Word document generation
- PDF generation
- Voucher download
- Payment validation business rules
- Windows application packaging
- Storing credentials

## 4. Runtime Requirements

Required:

```text
Python 3
requests
tkinter
```

`requests` is installed from `requirements.txt`.

Tkinter normally ships with standard Windows Python installations.

Install command:

```powershell
py -m pip install -r requirements.txt
```

Run command:

```powershell
py app\nezasa_fetch_ui.py
```

## 5. Main File

```text
app/nezasa_fetch_ui.py
```

This is the only active application file. Future improvements to Step 1 should
be made here unless the project deliberately introduces a package structure.

## 6. UI Fields

The GUI contains:

```text
Distribution Channel
API Username
Booking ID
API Key / Password
Fetch & Save JSON button
```

The Distribution Channel can optionally be prefilled through the
`NEZASA_DISTRIBUTION_CHANNEL` environment variable.

The password input uses a masked Tkinter entry:

```python
show="*"
```

## 7. Authentication

The Nezasa Booking API uses HTTP Basic Authentication.

The API username and password are entered by the user at runtime.

For local convenience, the username field can be prefilled through the
`NEZASA_API_USERNAME` environment variable.

Credentials must not be stored in:

- source code
- README files
- GitHub issues
- committed JSON files
- screenshots

OAuth Client ID and OAuth Client Secret from the TripBuilder OAuth
Configuration page are not used for this Booking API workflow.

## 8. Endpoint

The Booking API endpoint is:

```text
https://{distribution-channel}.tripbuilder.app/bookings/v1.13/{booking_id}
```

Example URL shape:

```text
https://example-channel.tripbuilder.app/bookings/v1.13/examplebookingid
```

There is no `/api/` segment in the URL.

Correct:

```text
/bookings/v1.13/{booking_id}
```

Wrong:

```text
/api/bookings/v1.13/{booking_id}
```

## 9. HTTP Request

The request uses:

```text
Method: GET
Header: Accept: application/vnd.api+json
Authentication: HTTP Basic Auth
Timeout: 30 seconds
```

Python implementation:

```python
requests.get(
    url,
    headers={"Accept": "application/vnd.api+json"},
    auth=HTTPBasicAuth(username, password),
    timeout=30,
)
```

## 10. Booking ID Handling

Booking IDs are sanitized before use:

- trim leading/trailing whitespace
- remove whitespace copied inside the ID
- normalize to lowercase
- keep only `a-z`, `0-9`, `_`, and `-`

The sanitized Booking ID is used in:

- the API URL
- the output filename

Output filename:

```text
booking_<booking_id>.json
```

## 11. Distribution Channel Handling

Distribution Channel input is sanitized before use:

- trim whitespace
- normalize to lowercase
- keep only `a-z`, `0-9`, and `-`

The field is required unless it is prefilled through the
`NEZASA_DISTRIBUTION_CHANNEL` environment variable.

The channel becomes the host prefix:

```text
{channel}.tripbuilder.app
```

Example:

```text
example-channel -> https://example-channel.tripbuilder.app
```

## 12. JSON Save Location

The current GUI saves to the detected Desktop directory.

Resolution order:

1. `%USERPROFILE%\Desktop`
2. `%USERPROFILE%\OneDrive\Desktop`
3. `%OneDrive%\Desktop`
4. user home directory fallback

This exists because Windows environments may redirect Desktop via OneDrive.

A future improvement may replace this with a Save As dialog.

## 13. Error Handling

The GUI reports errors with message boxes.

Known response meanings:

```text
200 -> success
401 -> authentication or BookingAPI role issue
404 -> wrong Booking ID, wrong Distribution Channel, or wrong endpoint
other -> show status code and response preview
```

For `401`, first check:

- username
- password
- whether the API user has the BookingAPI role

For `404`, first check:

- endpoint has no `/api/`
- Distribution Channel
- Booking ID

## 14. Data Protection

Returned JSON can contain:

- customer names
- addresses
- email addresses
- phone numbers
- passenger birth dates
- payment information
- booking references
- voucher URLs

For this reason:

- `*.json` is ignored by Git
- generated `.docx` and `.pdf` files are ignored by Git
- credentials must not be committed

If sanitized sample data is ever needed, add a deliberate exception in
`.gitignore` and clearly mark the sample as sanitized.

## 15. Repository Policy

The active repository should stay small.

Tracked files should be limited to:

```text
.gitattributes
.gitignore
README.md
SECURITY.md
docs/TECHNICAL_SPECIFICATION.md
requirements.txt
app/nezasa_fetch_ui.py
```

Old Word-generation experiments are intentionally not kept in the clean active
repository while JSON-to-Word is on hold.

## 16. Next Accepted Improvement Candidates

Do these one at a time and test after each change:

- add Save As dialog for the JSON output
- clear password field after successful fetch
- add a small status label in the GUI
- add unit tests for sanitization and URL generation
- split API logic from UI only if the file becomes hard to maintain

Do not start Word generation again until Step 1 is stable and accepted.
