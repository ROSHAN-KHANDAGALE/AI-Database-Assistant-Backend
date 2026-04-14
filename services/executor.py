from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

def validate_query(sql: str) -> None:
    sql_upper = sql.upper().strip()

    if sql_upper.startswith("INSERT"):
        raise ValueError("INSERT statements are not allowed.")
    if sql_upper.startswith("DROP"):
        raise ValueError("DROP statements are not allowed.")
    if sql_upper.startswith("DELETE") and "WHERE" not in sql_upper:
        raise ValueError("DELETE statements must have a WHERE clause.")
    

def inject_limit(sql: str, limit: int = 100) -> str:
    sql_upper = sql.upper()
    sql = sql.strip().rstrip(";")
    if "LIMIT" in sql_upper:
        return sql
    return f'{sql} LIMIT {limit}'


async def execute_query(sql: str, db: AsyncSession) -> list[dict]:
    validate_query(sql)
    sql_with_limit = inject_limit(sql)
    result = await db.execute(text(sql_with_limit))
    rows = result.fetchall()
    columns = list(result.keys())
    return [dict(zip(columns, row)) for row in rows]
