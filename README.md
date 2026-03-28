# Project Buddha MVP

Minimal geriatric patient data collection web app built with FastAPI, SQLAlchemy, and a lightweight browser UI.

## Features

- JWT authentication
- Seeded admin account
- Patient registration and search
- Visit creation and review
- Medication and assessment capture
- Audit logging for core data mutations

## Quick Start

1. Create a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
uvicorn app.main:app --reload
python -m uvicorn app.main:app --reload
```

4. Open `http://127.0.0.1:8000`

## Default Login

- Email: `admin@buddha.local`
- Password: `ChangeMe123!`

Change the seeded password before real use.

## Environment Variables

- `APP_NAME`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `DATABASE_URL`
- `FIRST_ADMIN_EMAIL`
- `FIRST_ADMIN_PASSWORD`

If `DATABASE_URL` is not provided, the app uses a local SQLite database at `./project_buddha.db`.

