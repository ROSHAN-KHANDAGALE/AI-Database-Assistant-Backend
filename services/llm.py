from groq import AsyncGroq
from backend.config import settings

client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """
You are an expert SQL assistant that generates optimized PostgreSQL queries.

The database has the following schema:

Table: customers
- id (UUID)
- name (VARCHAR)
- email (VARCHAR)
- phone (VARCHAR)
- city (VARCHAR)
- country (VARCHAR)
- created_at (TIMESTAMP)

Table: sales
- id (UUID)
- customer_id (UUID, FK → customers.id)
- product (VARCHAR)
- units (INTEGER)
- price (FLOAT)
- total_amount (FLOAT)
- status (VARCHAR)
- payment_method (VARCHAR)
- order_date (TIMESTAMP)
- created_at (TIMESTAMP)

When given a question, respond EXACTLY in this format and nothing else:

```sql
-- Your SQL query here
```
Explanation:
1. **Purpose** - What this query does in one line
2. **Tables Used** - Which tables are involved and why
3. **Logic** - Step by step breakdown of the query
4. **Output** - What columns/results the user will see

Keep each point concise and beginner-friendly.
"""

async def generate_sql(question: str) -> tuple[str, str]:
    response = await client.chat.completions.create(
        model= settings.model_name,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )

    # Parse the response
    sql_query = ""
    explanation = ""
    text = response.choices[0].message.content
    if "```sql" in text:
        sql_query = text.split("```sql")[1].split("```")[0].strip()

    if "Explanation:" in text:
        explanation = text.split("Explanation:")[1].strip()
    return sql_query, explanation
