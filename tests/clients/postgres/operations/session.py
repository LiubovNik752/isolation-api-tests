from tests.clients.postgres.session import get_postgres_test_session_factory
from tests.config import test_settings

# Фабрика сессий именно для Postgres базы operations-service.
operations_test_session_factory = get_postgres_test_session_factory(
    test_settings.operations_postgres_client,
)
