# SQL Query Assistant — Backend

An AI-powered backend that converts plain English questions into optimized PostgreSQL queries using Groq LLM.

---

## Tech Stack

- **FastAPI** — Web framework
- **PostgreSQL** — Database (managed via pgAdmin)
- **SQLAlchemy (Async)** — ORM
- **Groq (LLaMA 3.3)** — LLM for SQL generation
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

---

## Prerequisites

- Python 3.12+
- PostgreSQL installed and running
- pgAdmin (for DB management)
- Groq API key → https://console.groq.com

---

## Setup & Installation

```bash
# 1. Navigate to backend folder
cd ai-assistant/backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env.local file (see Environment Variables below)

# 6. Create database in pgAdmin
# Run: CREATE DATABASE assistant_db;

# 7. Start the server (from ai-assistant/ root)
cd ..
uvicorn backend.main:app --reload
```

---

## Environment Variables

Create `backend/.env.local`:

```
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql+asyncpg://username:yourpassword@localhost:5432/assistant_db
MODEL_NAME=your_groq_model_name
ALLOWED_ORIGINS=["http://localhost:3000"]
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/query/generate_query` | Send English question, get SQL + explanation |

### Example Request

```json
POST /query/
{
    "question": "Show top 5 customers by total sales amount"
}
```

### Example Response

```json
{
    "sql_query": "SELECT c.name, SUM(s.total_amount) AS total_sales FROM customers c JOIN sales s ON c.id = s.customer_id GROUP BY c.name ORDER BY total_sales DESC LIMIT 5;",
    "explanation": "1. **Purpose** - Retrieves top 5 customers by total sales...",
    "timestamp": "2026-04-13T16:57:51.459502Z"
}
```

---

## Database Schema

```
customers
  id            UUID        PK
  name          VARCHAR(255)
  email         VARCHAR(255) UNIQUE
  phone         VARCHAR(20)
  city          VARCHAR(100)
  country       VARCHAR(100)
  created_at    TIMESTAMPTZ

sales
  id              UUID        PK
  customer_id     UUID        FK → customers.id
  product         VARCHAR(255)
  units           INTEGER
  price           FLOAT
  total_amount    FLOAT
  status          VARCHAR(50)
  payment_method  VARCHAR(50)
  order_date      TIMESTAMPTZ
  created_at      TIMESTAMPTZ
```

---

## Project Structure

```
backend/
├── main.py          → FastAPI app, CORS, lifespan startup
├── config.py        → Environment variables via pydantic-settings
├── db.py            → Async SQLAlchemy engine and session
├── models.py        → ORM models (Customer, Sales)
├── schemas.py       → Pydantic request/response schemas
├── routers/
│   └── queries.py   → POST /query/ endpoint
└── services/
    └── llm.py       → Groq client, system prompt, SQL parsing
```

---

## Interactive API Docs

Once running, visit:
- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc