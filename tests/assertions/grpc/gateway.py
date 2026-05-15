from datetime import date

import allure

from contracts.services.accounts.account_pb2 import Account, AccountStatus, AccountType
from contracts.services.cards.card_pb2 import Card, CardPaymentSystem, CardStatus, CardType
from contracts.services.gateway.account_details_pb2 import AccountDetails
from contracts.services.gateway.rpc_get_account_details_pb2 import GetAccountDetailsResponse
from contracts.services.gateway.rpc_get_user_details_pb2 import GetUserDetailsResponse
from contracts.services.gateway.user_details_pb2 import UserDetails
from contracts.services.users.user_pb2 import User
from tests.assertions.base import assert_equal
from tests.assertions.grpc.accounts import assert_account
from tests.assertions.grpc.cards import assert_card
from tests.assertions.grpc.users import assert_user
from tests.tools.date import to_proto_test_date
from tests.tools.logger import get_test_logger
logger = get_test_logger("GATEWAY_ASSERTIONS")


@allure.step("Check user details")
def assert_user_details(actual: UserDetails, expected: UserDetails) -> None:
    logger.info("Check user details")

    assert_user(actual.user, expected.user)
    assert_equal(len(actual.accounts), len(expected.accounts), "accounts count")

    for index, account in enumerate(expected.accounts):
        assert_account(actual.accounts[index], account)


@allure.step("Check account details")
def assert_account_details(actual: AccountDetails, expected: AccountDetails) -> None:
    logger.info("Check account details")

    assert_account(actual.account, expected.account)
    assert_equal(len(actual.cards), len(expected.cards), "cards count")

    for index, card in enumerate(expected.cards):
        assert_card(actual.cards[index], card)


@allure.step("Check get user details response")
def assert_get_user_details_response(actual: GetUserDetailsResponse, expected: GetUserDetailsResponse) -> None:
    logger.info("Check get user details response")

    assert_user_details(actual.details, expected.details)


@allure.step("Check get account details response")
def assert_get_account_details_response(
        actual: GetAccountDetailsResponse,
        expected: GetAccountDetailsResponse
) -> None:
    logger.info("Check get account details response")

    assert_account_details(actual.details, expected.details)


@allure.step("Check get user details response. User with active credit card account")
def assert_get_user_details_response_user_with_active_credit_card_account(
        actual: GetUserDetailsResponse,
) -> None:
    logger.info("Check get user details response. User with active credit card account")

    expected = GetUserDetailsResponse(
        details=UserDetails(
            user=User(
                id="8b0e7c2a-1b6a-4e5d-9f1a-1b3f2a7c9e21",
                email="anna.ivanova@example.com",
                last_name="Иванова",
                first_name="Анна",
                middle_name="Алексеевна",
                phone_number="+79005554433",
            ),
            accounts=[
                Account(
                    id="99999999-aaaa-4bbb-8ccc-000000000001",
                    type=AccountType.ACCOUNT_TYPE_CREDIT_CARD,
                    status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
                    user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    balance=-15230.75,
                )
            ],
        )
    )
    assert_get_user_details_response(actual, expected)


@allure.step("Check get account details response. User with active debit card account")
def assert_get_account_details_response_user_with_active_debit_card_account(
        actual: GetUserDetailsResponse,
) -> None:
    logger.info("Check get account details response. User with active debit card account")

    expected = GetUserDetailsResponse(
        details=UserDetails(
            user=User(
                id="aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeedddd",
                email="anna.ivanova@example.com",
                last_name="Иванова",
                first_name="Анна",
                middle_name="Алексеевна",
                phone_number="+79005554433",
            ),
            accounts=[
                Account(
                    id="99999999-aaaa-4bbb-8ccc-000000000001",
                    type=AccountType.ACCOUNT_TYPE_DEBIT_CARD,
                    status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
                    user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    balance=777.88,
                )
            ],
        )
    )
    assert_get_user_details_response(actual, expected)
