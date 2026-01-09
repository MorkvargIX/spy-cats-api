# Spy cats API
This project is a backend service for the Spy Cat Agency management system.
It provides a REST API for managing spy cats, missions, and targets, including
validation and integration with external services.

## 🧱 Tech Stack

- **FastAPI** — REST API framework
- **SQLAlchemy 2.0 (async)** — ORM
- **SQLite** — database (for simplicity)
- **Pydantic v2** — request/response validation
- **HTTPX** — external API calls
- **Poetry** — dependency management

## 🗄 Database

The project uses **SQLite** as a lightweight database.
Tables are created automatically on application startup.

No manual migrations are required.

## 🐱 Breed Validation

Spy cat breeds are validated against **TheCatAPI**:
https://api.thecatapi.com/v1/breeds

If an invalid breed is provided, the API returns a validation error.

## 📁 Project Structure
```
app/
├── main.py          # FastAPI app entrypoint
├── routers/         # API routers
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── db/              # Database setup and session
├── dependencies/    # Dependency injection
```

## 🚀 Getting Started
### Prerequisites

- Python **3.13**
- `pip`
- `git`

# 🔧 Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

## ▶️ Run the application 

```bash
poetry run uvicorn app.main:app --reload
```

## The API will be available at:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* OpenAPI schema: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
* Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
