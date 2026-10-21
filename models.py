from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.db import Base


class UserInput(Base):
    __tablename__ = "user_inputs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
