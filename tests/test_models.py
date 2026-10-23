import unittest
import uuid

from sqlalchemy import Uuid

from backend.models import UserInput


class UserInputModelTests(unittest.TestCase):
    def test_primary_key_uses_uuid(self):
        column = UserInput.__table__.columns["id"]

        self.assertIsInstance(column.type, Uuid)
        self.assertTrue(column.type.as_uuid)
        self.assertIsInstance(column.default.arg(None), uuid.UUID)


if __name__ == "__main__":
    unittest.main()
