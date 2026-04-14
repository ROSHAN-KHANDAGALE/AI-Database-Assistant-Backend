from datetime import datetime, timezone
from pydantic import BaseModel, Field

class SQLQueryRequest(BaseModel):
    question: str = Field(...)

class SQLQueryResponse(BaseModel):
    sql_query: str
    explanation: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"from_attributes": True}

class QueryExecuteRequest(BaseModel):
    sql_query: str

class QueryExecuteResponse(BaseModel):
    sql_query: str
    results: list[dict]
    row_count: int
    error: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))