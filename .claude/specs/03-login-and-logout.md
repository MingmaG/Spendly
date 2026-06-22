



# Spec: Login and Logout

## Overview
Completes the authentication loop for Spendly. Login (`POST /login`) was already implemented as part of Step 02 (registration) — it verifies credentials and creates a session. This step fills the remaining gap: a working `/logout` route that clears the session, and a navbar that reflects whether a visitor is signed in (showing their name and a "Log out" link) instead of always showing "Sign in" / "Get started". Without this, a logged-in user has no way to end their session and `base.html` lies about their auth state on every page.

## Depends on
- Step 01 (database setup) — `users` table, `get_db()`.
- Step 02 (registration) — `POST /login` already creates `session["user_id"]`; this step does not change that route.

## Routes
- `GET /logout` — clear the session and redirect to `landing` — logged-in (safe no-op if already logged out)
  - Replaces the existing placeholder (`return "Logout — coming in Step 3"`) in `app.py`.

No other new routes. `/profile` and `/expenses/*` remain placeholders for later steps — not in scope here.

## Database changes
No schema changes. One new query function in `database/db.py`:
- `get_user_by_id(user_id)` — returns the matching row or `None`; used by the navbar context processor to look up the signed-in user's name from `session["user_id"]`.

## Templates
- **Create:** none.
- **Modify:** `templates/base.html` — the `nav-links` block currently always renders "Sign in" / "Get started". Change it to check the current user (injected via a Flask context processor, see below):
  - Logged out: keep existing "Sign in" / "Get started" links.
  - Logged in: show the user's name (plain text, not a link) and a "Log out" link pointing at `{{ url_for('logout') }}`.

## Files to change
- `app.py`:
  - Replace the placeholder `/logout` view: clear `session` (e.g. `session.pop("user_id", None)`) and `redirect(url_for("landing"))`.
  - Add a `@app.context_processor` function that reads `session.get("user_id")`, calls `get_user_by_id` if present, and injects a `current_user` variable (the row, or `None`) into every template render.
  - Import `get_user_by_id` from `database.db`.
- `database/db.py`: add `get_user_by_id(user_id)`.
- `templates/base.html`: conditional nav as described above.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — never use string formatting in SQL.
- Passwords hashed with `werkzeug.security` — unaffected by this step, but don't regress it.
- Use CSS variables — never hardcode hex values — if any new styling is touched (e.g. a small style for the signed-in name in the navbar).
- All templates extend `base.html` (no change needed here, but don't break this for existing pages).
- `/logout` must not error if no one is logged in — popping a missing session key should be a no-op, not a crash.
- Do not implement `/profile` or any `/expenses/*` route — those are intentional placeholders for later steps per `CLAUDE.md`.

## Definition of done
- [ ] Logging in via `/login`, then visiting `/logout`, redirects to the landing page and clears the session (confirmed by `/profile` no longer showing user-specific state, or by inspecting the session cookie).
- [ ] Visiting `/logout` while not logged in does not raise an error and redirects to the landing page.
- [ ] While logged out, the navbar on every page shows "Sign in" and "Get started" as before.
- [ ] While logged in, the navbar on every page shows the signed-in user's name and a "Log out" link instead of "Sign in" / "Get started".
- [ ] `app.py` runs with no errors on `python app.py`.
