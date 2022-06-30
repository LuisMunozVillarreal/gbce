"""gbce.models.trade module tests."""


from datetime import datetime, timedelta

import pytest
from pytest_factoryboy import register

from gbce.models.trade import TradeType

from .factories import TradeFactory

register(TradeFactory)


def test_repr(trade):
    """Method repr works."""
    # When / Then
    assert '<Trade "Buy" of Stock "TEA" object at ' in repr(trade)


def test_type(trade):
    """Get type works."""
    # When / Then
    assert trade.type == TradeType.BUY


def test_timestamp(trade_factory):
    """Get timestamp works."""
    # Given
    trade = trade_factory(timestamp=1000000000)

    # When / Then
    assert trade.timestamp == 1000000000


def test_not_expired(trade):
    """Is done last 5 minutes works with non expired trades."""
    # When / Then
    assert trade.is_done_last_5_minutes is True


@pytest.fixture
def timestamp(mocker):
    """Mock timestamp."""
    mock = mocker.patch("gbce.models.trade.datetime", wraps=datetime)
    mock.timestamp.return_value = datetime.timestamp(
        datetime.utcnow() + timedelta(minutes=5, seconds=1)
    )
    return mock


def test_expired(trade, timestamp):
    """Is done last 5 minutes works with expired trades."""
    # When / Then
    assert trade.is_done_last_5_minutes is False
