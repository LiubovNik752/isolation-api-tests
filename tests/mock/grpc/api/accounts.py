from pathlib import Path

from grpc.aio import ServicerContext

from contracts.services.cards.cards_service_pb2_grpc import CardsServiceServicer
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from tests.mock.grpc.tools import get_scenario_grpc
from tests.tools.logger import get_test_logger
from tests.tools.mock import MockLoader


loader = MockLoader(
    root=Path("./tests/mock/grpc/data/accounts"),
    logger=get_test_logger("ACCOUNTS_SERVICE_MOCK_LOADER")
)


class AccountsMockService(CardsServiceServicer):
    async def GetAccountsView(self, request: GetAccountsRequest, context: ServicerContext) -> GetAccountsResponse:
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetAccount/{scenario}.json",
            model=GetAccountsResponse
        )

    async def GetAccountView(self, request: GetAccountRequest, context: ServicerContext) -> GetAccountResponse:
        scenario = await get_scenario_grpc(context)

        return await loader.load_grpc(
            file=f"GetAccount/{scenario}.json",
            model=GetAccountResponse
        )