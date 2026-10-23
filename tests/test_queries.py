import unittest
from unittest.mock import AsyncMock, Mock, patch

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from backend.routers.queries import generate_query
from backend.schemas import SQLQueryRequest


class GenerateQueryTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.request = SQLQueryRequest(
            question="Show the latest projects",
            tables=[
                {
                    "table_name": "projects",
                    "columns": ["id", "created_at"],
                    "relationships": [],
                }
            ],
        )
        self.db = Mock()
        self.db.commit = AsyncMock()
        self.db.rollback = AsyncMock()

    @patch("backend.routers.queries.generate_sql", new_callable=AsyncMock)
    async def test_returns_generated_query(self, generate_sql):
        generate_sql.return_value = ("SELECT id FROM projects", "Project IDs")

        response = await generate_query(self.request, self.db)

        self.assertEqual(response.sql_query, "SELECT id FROM projects")
        self.assertEqual(response.explanation, "Project IDs")
        self.db.add.assert_called_once()
        self.db.commit.assert_awaited_once()

    @patch("backend.routers.queries.generate_sql", new_callable=AsyncMock)
    async def test_reports_database_save_failure(self, generate_sql):
        self.db.commit.side_effect = SQLAlchemyError("database error")

        with self.assertRaises(HTTPException) as error:
            await generate_query(self.request, self.db)

        self.assertEqual(error.exception.status_code, 503)
        self.assertIn("PostgreSQL", error.exception.detail)
        self.db.rollback.assert_awaited_once()
        generate_sql.assert_not_awaited()

    @patch("backend.routers.queries.generate_sql", new_callable=AsyncMock)
    async def test_reports_provider_failure(self, generate_sql):
        generate_sql.side_effect = ValueError("invalid provider response")

        with self.assertRaises(HTTPException) as error:
            await generate_query(self.request, self.db)

        self.assertEqual(error.exception.status_code, 502)
        self.assertIn("invalid response", error.exception.detail)


if __name__ == "__main__":
    unittest.main()
