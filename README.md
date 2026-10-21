# SQL Query Assistant API

FastAPI service for generating read-only SQL from a natural-language question and a supplied schema. Its PostgreSQL database stores submitted natural-language questions and their submission timestamps. It does not execute generated SQL or store schema metadata, uploaded SQL files, or generated SQL.

## Requirements

- Python 3.12+
- Groq API key
- PostgreSQL database for application input history

## Setup

From the project root:

```powershell
python -m venv backend\venv
backend\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Create `backend/.env.local`:

```text
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/assistant_db
MODEL_NAME=your_groq_model_name
ALLOWED_ORIGINS=["http://localhost:3000"]
```

Create the PostgreSQL database named in `DATABASE_URL` before starting the API. On startup, the API creates a `user_inputs` table with an ID, the submitted question, and a timestamp.

Start the API from the project root:

```powershell
uvicorn backend.main:app --reload
```

## API

`POST /query/generate_query` accepts a question and schema metadata:

```json
{
  "question": "Show each customer and their total order value",
  "tables": [
    {
      "table_name": "customers",
      "columns": ["id", "name"],
      "relationships": []
    },
    {
      "table_name": "orders",
      "columns": ["id", "customer_id", "total"],
      "relationships": ["customer_id -> customers.id"]
    }
  ]
}
```

The API receives schema metadata from the browser. It stores only the submitted natural-language question and timestamp in `user_inputs`. It does not store schema metadata, uploaded SQL files, row data, or generated SQL. It does not accept database credentials for the user's data source.

Interactive API documentation is available at `http://localhost:8000/docs`.


## Contributing and repository policies

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Security Policy](./SECURITY.md)
- [Bug Report](./.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request](./.github/ISSUE_TEMPLATE/feature_request.md)
- [Pull Request Template](./.github/PULL_REQUEST_TEMPLATE.md)

## License

No license has been selected for this repository. Until a license is added, do not assume permission to use, modify, or redistribute the code.