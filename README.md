<div align="center">

<h1>NutriTracker</h1>

**[WRITE: one-line tagline for the app]**

[WRITE: one sentence describing what the app does]

<br />

[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge)](http://localhost:8501)
[![Flask](https://img.shields.io/badge/API-Flask-000000?style=for-the-badge)](http://localhost:4000)
[![MySQL](https://img.shields.io/badge/Database-MySQL%209-4479A1?style=for-the-badge)](http://localhost:3200)

</div>

---

## The Problem

[WRITE: 2-3 sentences about why campus nutrition tracking sucks right now. What's broken? Why do students struggle?]

**NutriTracker fixes that.**

[WRITE: 2-3 sentences about what NutriTracker does differently]

---

## Team AJJR

| Name | Role | Persona |
|---|---|---|
| **Andrew Dickerson** | [FILL IN] | Jordan Carter (Performer) |
| **Jasmine O'Brien** | [FILL IN] | Jason Batum (Student-Athlete) |
| **Joshua Barrera** | [FILL IN] | Laura Smith (System Admin) |
| **Ryan Sinha** | [FILL IN] | Immanuel Hoffborne (Data Analyst) |

---

## Features

### For Students & Performers (Jordan)
[WRITE: 3-4 bullet points — Andrew's features]

### For Athletes (Jason)
[WRITE: 3-4 bullet points — Jasmine's features]

### For Data Analysts (Immanuel)
[WRITE: 3-4 bullet points — your features]

### For System Admins (Laura)
[WRITE: 3-4 bullet points — Joshua's features]

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| API | Flask (Python) |
| Database | MySQL 9 |
| Containerization | Docker Compose |

---

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/dickersonal-nu/26S-NutriTracker.git
   cd 26S-NutriTracker
   ```

2. **Create the `.env` file** in the `api/` folder:
   ```bash
   cat > api/.env << 'EOF'
   SECRET_KEY=your-secret-key-here
   DB_USER=root
   DB_HOST=db
   DB_PORT=3306
   DB_NAME=nutritracker
   MYSQL_ROOT_PASSWORD=your-password-here
   EOF
   ```
   Replace `your-secret-key-here` and `your-password-here` with any values you choose.

3. **Start all containers**
   ```bash
   docker compose up -d
   ```

4. **Open the app**
   - Streamlit UI: [http://localhost:8501](http://localhost:8501)
   - Flask API: [http://localhost:4000](http://localhost:4000)

5. **Log in** by selecting a persona from the home page — no password needed.

### Rebuilding the Database

If you change any SQL files, recreate the database container:
```bash
docker compose down db -v
docker compose up db -d
```

---

## Project Structure

```
26S-NutriTracker/
├── api/
│   ├── backend/
│   │   ├── analytics/          # [FILL IN: what's in here]
│   │   ├── nutrition/          # [FILL IN: what's in here]
│   │   ├── db_connection/      # MySQL connection helper
│   │   └── rest_entry.py       # Flask app factory + blueprint registration
│   ├── .env                    # Database credentials (not committed)
│   └── Dockerfile
├── app/
│   └── src/
│       ├── Home.py             # Landing page with persona selection
│       ├── pages/              # [FILL IN: how pages are organized]
│       └── modules/nav.py      # Sidebar navigation
├── database-files/
│   ├── 01_nutritracker_ddl.sql             # Schema
│   ├── 02_nutritracker_data.sql            # Seed data
│   └── 03_nutritracker_mock_analytics.sql  # [FILL IN: what's in here]
└── docker-compose.yaml
```

---

## Demo Video

[PASTE VIDEO LINK HERE — must be publicly accessible, no permission required]

---

<div align="center">

[WRITE: one closing line]

</div>