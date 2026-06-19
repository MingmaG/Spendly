# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" is a Flask-based expense tracker built incrementally as a step-by-step learning project. The app is scaffolded with placeholder routes and stub modules that get filled in one "Step" at a time (see comments in `app.py` and `database/db.py`). Do not assume unimplemented routes/functions are bugs — check whether they're an intentional placeholder for a later step before "fixing" them.

Current branch (`feature/database-setup`) corresponds to Step 1: implementing the database layer in `database/db.py`.

## Commands
                      
- Run the dev server: `python app.py` (serves on `http://localhost:5001`, debug mode on)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest` (uses `pytest` + `pytest-flask`; no test files exist yet — add `test_*.py` files at the repo root or in a `tests/` dir)
- Activate venv (PowerShell): `venv\Scripts\Activate.ps1`

## Architecture

- `app.py` — single Flask app with all routes defined directly (no blueprints). Routes render Jinja templates from `templates/`. Several routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) are placeholders returning plain strings — these are implemented in later steps, not yet wired to templates or the database.
- `database/db.py` — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables via `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample dev data). Currently a stub with no implementation.
- `templates/` — Jinja2 templates. `base.html` defines the shared layout (nav, footer) that other pages extend; `landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html` are the current pages.
- `static/css/style.css` and `static/js/main.js` — global styles/scripts shared across pages (vanilla JS/CSS, no build step, no frontend framework or package manager).
- SQLite is the database (`expense_tracker.db`, gitignored, created at runtime via `init_db()`).

## Conventions

- No JS frameworks or external frontend dependencies — vanilla JS/CSS only.
- Match existing page styling/theme when adding new templates rather than introducing a new visual style.
- `file.txt` in the repo root is a running log of prompts used to build prior features — not application code.
