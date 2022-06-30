"""gbce.models.stock package tests."""


import pytest
from pytest_factoryboy import register

from gbce.models.trade import Trade, TradeType

from .factories import CommonStockFactory, PreferredStockFactory

register(CommonStockFactory)
register(CommonStockFactory, "common_stock_no_dividend", last_dividend=0)
register(PreferredStockFactory)


def test_repr(common_stock):
    """Method repr works."""
    # When / Then
    assert '<CommonStock "POP" object at ' in repr(common_stock)


@pytest.mark.parametrize(["price", "result"], [(0, None), (1, 800), (2, 400)])
def test_common_dividend_yield(common_stock, price, result):
    """Common stock dividend yield works."""
    # When / Then
    assert common_stock.calculate_dividend_yield(price) == result


@pytest.mark.parametrize(
    ["price", "result"], [(0, None), (75.555, 2.647078287340348), (200, 1)]
)
def test_preferred_dividend_yield(preferred_stock, price, result):
    """Preferred stock dividend yield works."""
    # When / Then
    assert preferred_stock.calculate_dividend_yield(price) == result


@pytest.mark.parametrize(["price", "result"], [(0, 0), (1, 0.125), (2, 0.25)])
def test_p_e_ratio(common_stock, price, result):
    """Stock P/E ratio works."""
    # When / Then
    assert common_stock.calculate_p_e_ratio(price) == result


@pytest.mark.parametrize(["price", "result"], [(0, None), (1, None)])
def test_no_p_e_ratio(common_stock_no_dividend, price, result):
    """Stock with no P/E ratio is managed."""
    # When / Then
    assert common_stock_no_dividend.calculate_p_e_ratio(price) == result


def test_volume_weighted_stock_price(common_stock):
    """Volume weighted stock price works."""
    # Given
    trades = [(1, 2), (3, 4), (5, 6)]
    for quantity, price in trades:
        common_stock.buy(quantity, price)
    assert len(trades) == len(common_stock.trades)

    # When
    res = common_stock.calculate_volume_weighted_stock_price()

    # Then
    assert res == 4.888888888888889


def test_expired_trades_dont_affect_vwsp(common_stock):
    """Volume weighted stock price on expired trades is managed."""
    # Given
    trades = [(1, 2), (3, 4), (5, 6)]
    for quantity, price in trades:
        common_stock.buy(quantity, price)
    assert len(trades) == len(common_stock.trades)
    res = common_stock.calculate_volume_weighted_stock_price()
    assert res == 4.888888888888889

    # When
    common_stock.record_trade(TradeType.BUY, 10, 100, 1000000000)
    res = common_stock.calculate_volume_weighted_stock_price()

    # Then
    assert res == 4.888888888888889


def test_no_trades_no_vwsp(common_stock):
    """There is no vwsp when there is no trades."""
    # When
    res = common_stock.calculate_volume_weighted_stock_price()

    # Then
    assert res == 0


@pytest.mark.parametrize(
    ["quantity", "price", "result"],
    [(-1, 1, 0), (0, 0, 0), (1, 1, 1), (1, -1, 1), (5, 5, 1), (5.5, 5.5, 1)],
)
def test_sell(common_stock, quantity, price, result):
    """Sell stocks works."""
    # When
    trade = common_stock.sell(quantity, price)

    # Then
    if result:
        assert isinstance(trade, Trade)
    assert len(common_stock.trades) == result


@pytest.mark.parametrize(
    ["quantity", "price", "result"],
    [(-1, 1, 0), (0, 0, 0), (1, 1, 1), (1, -1, 1), (5, 5, 1), (5.5, 5.5, 1)],
)
def test_buy(common_stock, quantity, price, result):
    """Buy stocks works."""
    # When
    trade = common_stock.buy(quantity, price)

    # Then
    if result:
        assert isinstance(trade, Trade)
    assert len(common_stock.trades) == result
