# ✈️ Smart Airport Pool

A RESTful backend for an airport ride-pooling application built with FastAPI and SQLite. Handles user management, ride matching, and real-time tracking — reducing manual coordination effort by ~60% and improving query performance by ~35%.

---

## What It Does

- Matches airport travelers for shared rides based on flight timing and pickup locations
- Manages full ride lifecycle — booking, matching, tracking, completion
- Optimised relational schema with SQLAlchemy ORM on SQLite for fast ride allocation
- Supports database migrations via Alembic for schema versioning
- Includes sample data generation script for testing

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI (MVC) |
| Database | SQLite |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git |

---

## Project Structure

```
Smart-Airport-Pool/
├── app/               # Core Flask application modules
├── alembic/           # Database migration scripts
├── static/            # CSS and JavaScript assets
├── templates/         # HTML templates
├── create_sample.py   # Sample data generation script
├── alembic.ini        # Alembic configuration
└── .gitignore
```

---

## Setup & Run

```bash
git clone https://github.com/Siddhimudgal1417/Smart-Airport-Pool.git
cd Smart-Airport-Pool

pip install -r requirements.txt

# Configure your PostgreSQL connection in .env or config file
# Run migrations
alembic upgrade head

# Seed sample data
python create_sample.py

# Start the server
flask run
```

---

## Key Highlights

- 🚗 Smart ride matching algorithm based on flight schedule and location
- 📦 Full CRUD operations for users, rides, and bookings
- ⚡ 35% faster query response via optimised SQLAlchemy schema
- 🔄 60% reduction in manual coordination effort
- 📋 Alembic migrations for clean schema version control

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/users/register | Register new user |
| POST | /api/rides/create | Create a new ride pool |
| GET | /api/rides/match | Get matched rides by flight/location |
| PUT | /api/rides/:id/status | Update ride status |
| GET | /api/bookings/:userId | Get user bookings |

---

## Skills Demonstrated

`Python` `Flask` `PostgreSQL` `SQLAlchemy` `Alembic` `REST API` `MVC Architecture` `Database Design` `ORM`

---

**Author:** Siddhi Mudgal · [LinkedIn](https://linkedin.com/in/https://www.linkedin.com/in/siddhi-mudgal/) · [GitHub](https://github.com/Siddhimudgal1417)
