from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from tests.tools.config.postgres import PostgresClientTestConfig


def get_postgres_test_session_factory(config: PostgresClientTestConfig) -> sessionmaker[Session]:
    """
    Фабрика создания sessionmaker для тестового слоя.

    Это единственное место, где:
    - создаётся SQLAlchemy engine;
    - применяется конфигурация подключения к Postgres;
    - фиксируется поведение ORM-сессий в тестах.

    Тестовый код и repository:
    - не знают, откуда берётся DSN;
    - не читают переменные окружения напрямую;
    - работают только с типизированной конфигурацией тестового окружения.
    """

    engine = create_engine(
        url=str(config.dsn),
        echo=config.echo,
        future=True,
        pool_pre_ping=True,
    )

    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )