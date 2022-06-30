"""factories module."""


import logging
from datetime import datetime

import factory

from gbce.models.stock.common import CommonStock
from gbce.models.stock.preferred import PreferredStock
from gbce.models.trade import Trade, TradeType


class CommonStockFactory(factory.Factory):
    """CommonStock factory class."""

    # pylint: disable=too-few-public-methods

    class Meta:
        """CommonStock factory meta class."""

        model = CommonStock

    logger_level = logging.DEBUG
    name = "POP"
    last_dividend = 8
    fixed_dividend = None
    par_value = 100


class PreferredStockFactory(factory.Factory):
    """PreferredStock factory class."""

    # pylint: disable=too-few-public-methods

    class Meta:
        """PreferredStock factory meta class."""

        model = PreferredStock

    logger_level = logging.DEBUG
    name = "GIN"
    last_dividend = 8
    fixed_dividend = 2
    par_value = 100


class TradeFactory(factory.Factory):
    """Trade factory class."""

    # pylint: disable=too-few-public-methods

    class Meta:
        """Trade factory meta class."""

        model = Trade

    stock_name = "TEA"
    quantity = 2.3
    trade_type = TradeType.BUY
    price = 4.5
    timestamp = datetime.timestamp(datetime.utcnow())
