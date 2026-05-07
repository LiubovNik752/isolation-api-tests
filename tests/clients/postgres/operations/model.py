import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime, Float, String
from sqlalchemy.orm import Mapped

from tests.clients.postgres.base import BaseTestModel


class OperationsTestModel(BaseTestModel):
    """
    ORM-модель таблицы operations в Postgres.

    Важный принцип курса:
    - мы не придумываем структуру данных;
    - мы отражаем реальную схему таблицы в тестовом стенде.

    Эта модель описывает "как операция хранится в БД"
    в рамках стенда, чтобы тестовый слой мог
    подготовить состояние для проверок синхронных API.

    При необходимости сверяйтесь с pgAdmin:
    таблица operations — источник правды
    по именам полей и типам колонок.
    """
    __tablename__ = "operations"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True)
    type: Mapped[str] = Column(String(length=50), nullable=False)
    status: Mapped[str] = Column(String(length=50), nullable=False)
    amount: Mapped[float] = Column(Float, nullable=False)
    user_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    card_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    account_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    category: Mapped[str] = Column(String(length=50), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
