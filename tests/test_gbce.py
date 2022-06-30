"""gbce package tests."""


import copy

import pytest

from gbce import Gbce

from .fixtures.stocks import SAMPLE_STOCKS


def test_add_stocks():
    """GBCE can add stocks."""
    # Given
    gbce = Gbce()
    stocks = copy.deepcopy(SAMPLE_STOCKS)

    # When
    for key, values in stocks.items():
        values["name"] = key
        values["stock_type"] = values.pop("type")
        gbce.add_stock(**values)  # pylint: disable=unexpected-keyword-arg

    # Then
    count = len(gbce.stocks)
    assert count
    assert count == len(SAMPLE_STOCKS)


@pytest.fixture
def stock_values():
    """Get stock set of values."""
    stocks = copy.deepcopy(SAMPLE_STOCKS)
    name = "TEA"
    values = stocks[name]
    values["name"] = name
    values["stock_type"] = values.pop("type")
    return values


@pytest.fixture
def gbce_with_a_stock(stock_values):
    """GBCE with a stock."""
    gbce = Gbce()
    gbce.add_stock(**stock_values)
    assert len(gbce.stocks) == 1
    return gbce


def test_add_already_existing_stock(gbce_with_a_stock, stock_values):
    """Add an already existing stock is managed."""
    # When
    res = gbce_with_a_stock.add_stock(**stock_values)

    # Then
    assert len(gbce_with_a_stock.stocks) == 1
    assert res is None


def test_add_invalid_stock_type():
    """Invalid stock type is not allowed."""
    # Given
    gbce = Gbce()

    # When
    res = gbce.add_stock("name", "invalid", 0, 0, 0)

    # Then
    assert res is None


def test_calculate_all_share_index(faker):
    """Calculate all share index works."""
    # Given
    gbce = Gbce()
    stocks = copy.deepcopy(SAMPLE_STOCKS)
    for key, values in stocks.items():
        values["name"] = key
        values["stock_type"] = values.pop("type")
        # pylint: disable=unexpected-keyword-arg
        stock = gbce.add_stock(**values)
        # pylint: enable=unexpected-keyword-arg
        for _ in range(faker.pyint(min_value=1, max_value=9)):
            if faker.pybool():
                stock.sell(
                    faker.pyfloat(left_digits=2, right_digits=2),
                    faker.pyfloat(left_digits=2, right_digits=2),
                )
            else:
                stock.buy(
                    faker.pyfloat(left_digits=2, right_digits=2),
                    faker.pyfloat(left_digits=2, right_digits=2),
                )

    # When
    res = gbce.calculate_all_share_index()

    # Then
    assert res == 20.115225729057688
