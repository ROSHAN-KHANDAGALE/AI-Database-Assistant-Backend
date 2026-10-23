import logging

from fastapi import APIRouter, Depends, HTTPException
from groq import APIError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.models import UserInput
from backend.schemas import SQLQueryRequest, SQLQueryResponse
from backend.services.llm import generate_sql

router = APIRouter(prefix="/query", tags=["Query"])
logger = logging.getLogger(__name__)


@router.post("/generate_query", response_model=SQLQueryResponse)
async def generate_query(
    body: SQLQueryRequest,
    db: AsyncSession = Depends(get_db),
):
    db.add(UserInput(question=body.question))
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        logger.exception("Failed to save the submitted question.")
        raise HTTPException(
            status_code=503,
            detail=(
                "Could not save your question to PostgreSQL. Check the database "
                "connection and user_inputs table."
            ),
        ) from exc

    try:
        sql_query, explanation = await generate_sql(body.question, body.tables)
    except APIError as exc:
        logger.exception("The SQL generation provider request failed.")
        raise HTTPException(
            status_code=502,
            detail=(
                "The SQL generation provider could not complete the request. "
                "Check the backend model name, API key, and provider availability."
            ),
        ) from exc
    except ValueError as exc:
        logger.exception("The SQL generation provider returned an invalid response.")
        raise HTTPException(
            status_code=502,
            detail="The SQL generation provider returned an invalid response. Please try again.",
        ) from exc

    return SQLQueryResponse(sql_query=sql_query, explanation=explanation)