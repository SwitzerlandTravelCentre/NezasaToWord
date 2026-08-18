# Security

This repository is public.

Do not commit:

- Nezasa / TripBuilder API usernames
- API passwords, keys, tokens, OAuth client secrets, or `.env` files
- raw booking JSON files
- generated Word or PDF travel documents
- customer names, addresses, email addresses, phone numbers, birth dates, or
  payment information

The application handles credentials only at runtime. Credentials must not be
stored in source code, documentation, screenshots, issues, or pull requests.

Generated booking data is ignored by `.gitignore`. If a sample file is ever
needed for tests or documentation, it must be synthetic or fully anonymized and
clearly marked as such.
