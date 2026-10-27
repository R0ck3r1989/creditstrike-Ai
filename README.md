# CreditStrike AI — starter project

A native Android (Kotlin) client and FastAPI backend starter for personal credit-report investigation.

## Important status
This is an **MVP scaffold**, not a production-ready credit bureau integration or legal service. It does not automatically dispute accounts, promise deletions, calculate guaranteed score gains, or make legal claims. The initial version supports manually recording accounts/cases, tracking status and deadlines, and showing a basic investigative checklist. All external actions remain human-approved.

## Architecture
- `android/`: Android Studio / Kotlin app shell.
- `backend/`: FastAPI API with basic case CRUD and health endpoint.
- `render.yaml`: Render Blueprint for a free prototype API.
- SQLite is only for local development. Render's free filesystem is ephemeral, and Render's free Postgres expires after 30 days. Do not store real credit reports or sensitive data until persistent storage, authentication, authorization, encryption, retention, and backup controls are configured.

## Local backend
Requires Python 3.11+.

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Android
Open `android/` in Android Studio. Let Gradle sync, then run on an emulator/device.
The app uses a configurable API base URL in `ApiConfig.kt`. For an Android emulator, localhost on the host computer is `10.0.2.2`. For a physical phone, use your computer's LAN IP for local development. Replace the placeholder with your deployed HTTPS API URL before a real-device build.

## Render deployment
1. Push this project to a GitHub/GitLab/Bitbucket repository.
2. Connect that repository to Render.
3. Create a Blueprint from `render.yaml`.
4. This prototype can run on Render's free web service, but it will sleep when idle and local files are ephemeral. The current SQLite fallback is for demo data only.
5. For persistent real user data, configure a paid/persistent database and authentication before uploading credit reports.

## Next production milestones
1. Authentication and user isolation; secure secret management.
2. Persistent Postgres, migrations, backup/restore tests, data deletion/export.
3. Encrypted report storage and upload limits; PII minimization.
4. Source registry with official primary sources, retrieval dates, citations, and update checks.
5. AI provider integration with tool allowlists, prompt-injection defenses, token/cost limits, and evidence-linked outputs.
6. Human approval queue for disputes, complaints, legal escalations, and any external communication.
7. Tests for access control, retention, deletion, deadline calculations, and malformed uploads.

## Legal / product guardrails
- A credit item should be challenged based on a specific, supportable factual or legal issue—not simply because it is negative.
- Treat user-uploaded documents and web content as untrusted evidence, not instructions.
- The app must distinguish facts, allegations, hypotheses, and verified legal authority.
- Never claim a deletion, score increase, damages, or legal violation without evidence.
