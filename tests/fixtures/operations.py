import pytest

from tests.clients.grpc.operations.client import (
    build_operations_grpc_test_client,
    OperationsGRPCTestClient,
)
from tests.clients.http.operations.client import (
    build_operations_http_test_client,
    OperationsHTTPTestClient,
)
from tests.clients.kafka.operations.producer import (
    OperationsKafkaProducerTestClient,
    build_operations_kafka_producer_test_client,
)
from tests.clients.postgres.operations.repository import (
    OperationsPostgresTestRepository,
    get_operations_postgres_test_repository,
)


@pytest.fixture
def operations_http_test_client() -> OperationsHTTPTestClient:
    return build_operations_http_test_client()


@pytest.fixture
def operations_grpc_test_client() -> OperationsGRPCTestClient:
    return build_operations_grpc_test_client()


@pytest.fixture
def operations_postgres_test_repository() -> OperationsPostgresTestRepository:
    return get_operations_postgres_test_repository()


@pytest.fixture
def operations_kafka_producer_test_client() -> OperationsKafkaProducerTestClient:
    return build_operations_kafka_producer_test_client()
