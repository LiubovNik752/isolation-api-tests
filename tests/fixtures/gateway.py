import pytest

from tests.clients.grpc.gateway.client import (
    GatewayGRPCTestClient,
    build_gateway_grpc_test_client,
)
from tests.clients.http.gateway.client import (
    GatewayHTTPTestClient,
    build_gateway_http_test_client,
)


@pytest.fixture
def gateway_http_test_client() -> GatewayHTTPTestClient:
    return build_gateway_http_test_client()


@pytest.fixture
def gateway_grpc_test_client() -> GatewayGRPCTestClient:
    return build_gateway_grpc_test_client()
