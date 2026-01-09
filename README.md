# spy-cats-api
This project is a backend service for the Spy Cat Agency management system.
It provides a REST API for managing spy cats, missions, and targets, including
validation and integration with external services.

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