pytest_plugins = [
    "ecommerce.tests.fixtures",
    "ecommerce.tests.selenium",
    "ecommerce.tests.factories",
    "ecommerce.tests.api_client_fixture",
    "ecommerce.tests.inventory_fixtures",
    "ecommerce.tests.promotion_fixtures",
    "celery.contrib.pytest",
]
