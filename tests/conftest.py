"""gbce test configuration module."""


import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    """Faker seed."""
    return "gbce"
