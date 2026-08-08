# TrekBase

Trekking applications (bookings, treks, staff) management system.

- **Backend:** Flask + SQLAlchemy + JWT auth
- **Frontend:** Vue 3 + Vite + Bootstrap 5
- **Caching:** Redis
- **Scheduled jobs:** Celery + beat
- **Email:** Mailpit (local test SMTP + inbox UI)

---

## Running services

### 1. Redis

```bash
docker run -d --name redis -p 6379:6379 redis:latest
```

### 2. Backend

```bash
cd backend
.venv/bin/python app.py
```

API is on `http://localhost:5000`.

### 3. Frontend

```bash
cd frontend
npm run dev
```

(or `bun run dev`) — Site on `http://localhost:5173`.

### 4. Celery (worker + beat scheduler)

(make sure the .venv is active)

```bash
cd backend
celery -A celery_app.celery_app worker --beat --loglevel=INFO
```

- **Daily at 07:00** the trek-reminder job runs.
- **1st of every month at 08:00** the admin report job runs.

### 5. Mailpit (email inbox)

```bash
docker run -d --name trekbase-mailpit -p 1025:1025 -p 8025:8025 axllent/mailpit
```

- SMTP: `localhost:1025` (used by the jobs to send email)
- View/receive emails at `http://localhost:8025`