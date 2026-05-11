# MedLink Workspace

This repository is organized as a small multi-app workspace:

- [frontend/](frontend) contains the Next.js user interface.
- [medlink-fastapi/](medlink-fastapi) contains the FastAPI backend.
- [medplum-main/](medplum-main) is a separate Medplum codebase kept alongside the main app.

The backend-specific documentation lives in [medlink-fastapi/README.md](medlink-fastapi/README.md), and the frontend starter notes live in [frontend/README.md](frontend/README.md).

## Local setup

Run each app from its own folder so the project stays cleanly separated.

Backend:

```powershell
Set-Location medlink-fastapi
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m pytest -q tests
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Frontend:

```powershell
Set-Location frontend
npm install
npm run dev
```

## Notes

The root README is intentionally kept as workspace-level documentation so the backend and frontend are no longer duplicated at the top level.
