from datetime import date

import allure

from tests.assertions.base import assert_equal
from tests.assertions.http.accounts import assert_account
from tests.assertions.http.cards import assert_card
from tests.assertions.http.users import assert_user
from tests.schema.accounts import AccountTestSchema
from tests.schema.cards import CardTestSchema
from tests.schema.gateway import (
    UserDetailsTestSchema,
    AccountDetailsTestSchema,
    GetUserDetailsResponseTestSchema,
    GetAccountDetailsResponseTestSchema
)
from tests.schema.users import UserTestSchema
from tests.tools.logger import get_test_logger
from tests.types.accounts import AccountTestType, AccountTestStatus
from tests.types.cards import CardTestPaymentSystem, CardTestStatus, CardTestType

logger = get_test_logger("GATEWAY_ASSERTIONS")


@allure.step("Check user details")
def assert_user_details(actual: UserDetailsTestSchema, expected: UserDetailsTestSchema) -> None:
    logger.info("Check user details")

    assert_user(actual.user, expected.user)
    assert_equal(len(actual.accounts), len(expected.accounts), "accounts count")

    for index, account in enumerate(expected.accounts):
        assert_account(actual.accounts[index], account)


@allure.step("Check account details")
def assert_account_details(actual: AccountDetailsTestSchema, expected: AccountDetailsTestSchema) -> None:
    logger.info("Check account details")

    assert_account(actual.account, expected.account)
    assert_equal(len(actual.cards), len(expected.cards), "cards count")

    for index, card in enumerate(expected.cards):
        assert_card(actual.cards[index], card)


@allure.step("Check get user details response")
def assert_get_user_details_response(
        actual: GetUserDetailsResponseTestSchema,
        expected: GetUserDetailsResponseTestSchema
) -> None:
    logger.info("Check get user details response")

    assert_user_details(actual.details, expected.details)


@allure.step("Check get account details response")
def assert_get_account_details_response(
        actual: GetAccountDetailsResponseTestSchema,
        expected: GetAccountDetailsResponseTestSchema
) -> None:
    logger.info("Check get account details response")

    assert_account_details(actual.details, expected.details)


@allure.step("Check get user details response. User with active credit card account")
def assert_get_user_details_response_user_with_active_credit_card_account(
        actual: GetUserDetailsResponseTestSchema,
) -> None:
    logger.info("Check get user details response. User with active credit card account")

    expected = GetUserDetailsResponseTestSchema(
        details=UserDetailsTestSchema(
            user=UserTestSchema(
                id="8b0e7c2a-1b6a-4e5d-9f1a-1b3f2a7c9e21",
                email="anna.ivanova@example.com",
                last_name="Иванова",
                first_name="Анна",
                middle_name="Алексеевна",
                phone_number="+79005554433",
            ),
            accounts=[
                AccountTestSchema(
                    id="99999999-aaaa-4bbb-8ccc-000000000001",
                    type=AccountTestType.CREDIT_CARD,
                    status=AccountTestStatus.ACTIVE,
                    user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    balance=-15230.75,
                )
            ],
        )
    )
    assert_get_user_details_response(actual, expected)


@allure.step("Check get account details response. User with active debit card account")
def assert_get_account_details_response_user_with_active_debit_card_account(
        actual: GetAccountDetailsResponseTestSchema,
) -> None:
    logger.info("Check get account details response. User with active debit card account")

    expected = GetAccountDetailsResponseTestSchema(
        details=AccountDetailsTestSchema(
            account=AccountTestSchema(
                id="99999999-aaaa-4bbb-8ccc-000000000001",
                type=AccountTestType.DEBIT_CARD,
                status=AccountTestStatus.ACTIVE,
                user_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                balance=-15230.75,
            ),
            cards=[
                CardTestSchema(
                    id="11111111-aaaa-4bbb-8ccc-222222222222",
                    pin="1234",
                    cvv="456",
                    type=CardTestType.VIRTUAL,
                    status=CardTestStatus.ACTIVE,
                    account_id="aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                    card_number="4111111111111111",
                    card_holder="IVAN PETROV",
                    expiry_date=date(2027, 12, 31),
                    payment_system=CardTestPaymentSystem.VISA,
                ),
                CardTestSchema(
                    id="33333333-dddd-4eee-8fff-444444444444",
                    pin="9876",
                    cvv="789",
                    type=CardTestType.PHYSICAL,
                    status=CardTestStatus.ACTIVE,
                    account_id="aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
                    card_number="5500000000000004",
                    card_holder="IVAN PETROV",
                    expiry_date=date(2028, 6, 30),
                    payment_system=CardTestPaymentSystem.MASTERCARD,
                ),
            ],
        )
    )
    assert_get_account_details_response(actual, expected)
