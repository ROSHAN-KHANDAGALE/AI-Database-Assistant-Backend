from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas import SQLQueryRequest, SQLQueryResponse, QueryExecuteRequest, QueryExecuteResponse
from backend.db import get_db
from backend.services.llm import generate_sql
from backend.services.executor import execute_query

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/generate_query", response_model=SQLQueryResponse)
async def generate_query(body: SQLQueryRequest):
    sql_query, explanation = await generate_sql(body.question)
    return SQLQueryResponse(sql_query=sql_query, explanation=explanation)


@router.post("/execute", response_model=QueryExecuteResponse)
async def execute_query_route(body: QueryExecuteRequest, db: AsyncSession = Depends(get_db)):
    try:
        results = await execute_query(body.sql_query, db)
        return QueryExecuteResponse(sql_query=body.sql_query, results=results, row_count=len(results))
    except ValueError as e:
        return QueryExecuteResponse(sql_query=body.sql_query, results=[], row_count=0, error=str(e))