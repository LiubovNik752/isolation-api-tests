import allure

from tests.assertions.base import assert_equal
from tests.schema.users import UserTestSchema
from tests.tools.logger import get_test_logger

logger = get_test_logger("USERS_ASSERTIONS")


@allure.step("Check user")
def assert_user(actual: UserTestSchema, expected: UserTestSchema) -> None:
    logger.info("Check user")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")
    assert_equal(actual.phone_number, expected.phone_number, "phone_number")
