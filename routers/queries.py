from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.models import UserInput
from backend.schemas import SQLQueryRequest, SQLQueryResponse
from backend.services.llm import generate_sql

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/generate_query", response_model=SQLQueryResponse)
async def generate_query(
    body: SQLQueryRequest,
    db: AsyncSession = Depends(get_db),
):
    db.add(UserInput(question=body.question))
    await db.commit()

    sql_query, explanation = await generate_sql(
        body.question,
        body.tables,
    )
    return SQLQueryResponse(sql_query=sql_query, explanation=explanation)