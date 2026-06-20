# Spec: Registration

## Overview
Implements account creation for Spendly. Visitors fill out the existing `register.html` form, the server validates the input, hashes the password, and inserts a new row into `users`. On success the user is redirected to `/login` to sign in with their new credentials — registration does not auto-create a session. This is the first feature step that turns a static page into a working flow.

Redirecting registration to `/login` exposed that `/login` had no `POST` handler (the existing form posted there but got a 405). To make the register → login flow actually work end-to-end, this spec also covers adding login: verifying credentials and creating the session.

## Depends on
- Step 1 (database setup) — `users` table, `get_db()`, `init_db()` must already exist and work. Confirmed implemented in `database/db.py`.

## Routes
- `POST /register` — accept form submission, validate input, create user, redirect to `/login` — public
  - Note: `/register` already exists as a GET-only route rendering `register.html`. This spec extends it to accept both `GET` and `POST` on the same view function rather than adding a second route.

No other new routes.

## Database changes
No schema changes — the existing `users` table (`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) already supports registration as defined in `database/db.py`.

Two new query functions are needed in `database/db.py` (data-access only, no schema change):
- `get_user_by_email(email)` — returns the matching row or `None`; used to check for duplicate emails before insert.
- `create_user(name, email, password_hash)` — inserts a new row into `users` and returns the new `user_id`.

## Templates
- **Create:** none — `templates/register.html` already has the form (`name`, `email`, `password` fields, `action="/register"`, and an `{% if error %}` block).
- **Modify:** `templates/register.html` — no structural changes expected; re-populate `{{ error }}` with server-side validation messages on failed submission (e.g. duplicate email, password too short). Re-render the form with previously entered `name`/`email` values on error so the user doesn't retype everything.

## Files to change
- `app.py`:
  - Update the `/register` view to accept `methods=["GET", "POST"]`.
  - On `POST`: validate fields, check for existing email via `get_user_by_email`, hash the password with `werkzeug.security.generate_password_hash`, call `create_user`, redirect to `/login`.
  - On validation failure: re-render `register.html` with an `error` message (and submitted `name`/`email` to repopulate the form).
- `database/db.py`: add `get_user_by_email(email)` and `create_user(name, email, password_hash)`.

## Files to create
None.

## New dependencies
No new dependencies — `werkzeug.security` (password hashing) is already available.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — never use string formatting in SQL.
- Passwords hashed with `werkzeug.security.generate_password_hash` before storage; never store plaintext.
- Use CSS variables — never hardcode hex values — if any new styling is touched.
- All templates extend `base.html`.
- Validate on the server even though the form has HTML5 `required`/`type` attributes (those are not trustworthy on their own).
- Duplicate email must be rejected with a user-facing error, not a raw `sqlite3.IntegrityError` traceback.
- Registration does not create a session — the user must sign in via `/login` after registering.

## Definition of done
- [ ] Submitting `register.html` with a new name/email/password creates a row in `users` with a hashed (not plaintext) password.
- [ ] After successful registration, the browser is redirected to `/login` and no session is created.
- [ ] Submitting with an email that already exists re-renders `register.html` with an error message and does not create a duplicate row.
- [ ] Submitting with a missing field or password under 8 characters re-renders `register.html` with an error message and does not hit the database.
- [ ] Visiting `GET /register` still renders the empty form as before.
- [ ] `app.py` runs with no errors on `python app.py`.
