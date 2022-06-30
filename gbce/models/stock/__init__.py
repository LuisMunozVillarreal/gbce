"""Stock model module."""


import logging
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Union

from gbce.logger import LoggerMixin

from ..trade import Trade, TradeType


class StockType(Enum):
    """Stock type class."""

    COMMON = "Common"
    PREFERRED = "Preferred"


class Stock(LoggerMixin, ABC):
    """Stock model class.

    Args:
        name (str): stock name.
        last_dividend (float): stock last dividend.
        fixed_dividend (float): stock fixed dividend.
        par_value (float): stock par value.
        logger_level (int): logger level.
    """

    _trades: list[Trade]

    def __init__(
        self,
        name: str,
        last_dividend: float,
        fixed_dividend: float,
        par_value: float,
        logger_level: int = logging.INFO,
    ):
        # pylint: disable=too-many-arguments
        super().__init__(logger_level)

        self._name = name
        self._last_dividend = last_dividend
        self._fixed_dividend = fixed_dividend
        self._par_value = par_value

        self._trades = []

    def __repr__(self) -> str:
        """Get representation of a Stock object.

        Returns:
            str: representation of a Stock object.
        """
        return (
            f'<{self.__class__.__qualname__} "{self._name}" '
            f"object at {hex(id(self))}>"
        )

    @property
    def trades(self) -> list[Trade]:
        """Get stock trades.

        Returns:
            list[Trade]: stock trades.
        """
        return self._trades

    @abstractmethod
    def _calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield of the stock.

        Args:
            price (float): preferred stock price.

        Returns:
            float: dividend yield percentage.
        """

    def calculate_dividend_yield(self, price: float) -> Union[float, None]:
        """Check price and calculate the dividend yield of the stock.

        Args:
            price (float): stock price.

        According to this
        https://www.sapling.com/7390209/can-dividend-yield-negative
        a dividend yield can't be negative. Therefore, negative prices
        aren't allowed.

        Returns:
            float: dividend yield percentage.
            bool: if price is 0.
        """
        if not price:
            self._log.warning(
                "%s: No dividend yield for price zero.", self._name
            )
            return None

        return self._calculate_dividend_yield(price)

    def calculate_p_e_ratio(self, price: float) -> Union[float, None]:
        """Calculate P/E ratio.

        Args:
            price (float): stock price.

        Returns:
            float: P/E ratio.
            None: if last dividend is zero.
        """
        if not self._last_dividend:
            self._log.info(
                "%s: No P/E ratio since the last dividend is zero",
                self._name,
            )
            return None

        return price / self._last_dividend

    def calculate_volume_weighted_stock_price(self) -> float:
        """Calculate volume weighted stock price.

        Returns:
            float: volume weighted stock price.
        """
        summation_price_x_qty = 0.0
        summation_quantity = 0.0

        for trade in self._trades:
            if trade.is_done_last_5_minutes:
                summation_price_x_qty += trade.price * trade.quantity
                summation_quantity += trade.quantity

        if not summation_quantity:
            return 0

        return summation_price_x_qty / summation_quantity

    def sell(self, quantity: float, price: float) -> Union[Trade, None]:
        """Sell stock.

        Args:
            quantity (float): quantity to sell.
            price (float): sell price.

        Returns:
            Trade: sell trade.
            None: if quantity is equal or lower than 0.
        """
        return self.record_trade(TradeType.SELL, quantity, price)

    def buy(self, quantity: float, price: float) -> Union[Trade, None]:
        """Buy stock.

        Args:
            quantity (float): quantity to buy.
            price (float): buying price.

        Returns:
            Trade: buying trade.
            None: if quantity is equal or lower than 0.
        """
        return self.record_trade(TradeType.BUY, quantity, price)

    def record_trade(
        self,
        trade_type: TradeType,
        quantity: float,
        price: float,
        timestamp: float = datetime.timestamp(datetime.utcnow()),
    ) -> Union[Trade, None]:
        """Record trade.

        Args:
            trade_type (TradeType): trade type
            quantity (float): quantity to trade.
            price (float): trade price.
            timestamp (float): date and time of the trade.

        Returns:
            Trade: buying trade.
            None: if quantity is equal or lower than 0.
        """
        if quantity <= 0:
            self._log.warning(
                "%s: Quantity needs to be bigger than 0", self._name
            )
            return None

        trade = Trade(self._name, trade_type, quantity, price, timestamp)
        self._trades.append(trade)

        return trade
