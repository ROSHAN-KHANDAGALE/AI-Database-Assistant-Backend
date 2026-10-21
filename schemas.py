from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TableSchema(BaseModel):
    table_name: str = Field(min_length=1, max_length=256)
    columns: list[str] = Field(min_length=1, max_length=256)
    relationships: list[str] = Field(default_factory=list, max_length=256)


class SQLQueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    tables: list[TableSchema] = Field(min_length=1, max_length=100)


class SQLQueryResponse(BaseModel):
    sql_query: str
    explanation: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"from_attributes": True}