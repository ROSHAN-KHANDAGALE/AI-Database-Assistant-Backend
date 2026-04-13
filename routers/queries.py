from fastapi import APIRouter
from backend.schemas import SQLQueryRequest, SQLQueryResponse
from backend.services.llm import generate_sql

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/generate_query", response_model=SQLQueryResponse)
async def generate_query(body: SQLQueryRequest):
    sql_query, explanation = await generate_sql(body.question)
    return SQLQueryResponse(sql_query=sql_query, explanation=explanation)
