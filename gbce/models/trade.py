"""Trade model.module."""


from datetime import datetime
from enum import Enum


class TradeType(Enum):
    """Trade type class."""

    BUY = "Buy"
    SELL = "Sell"


class Trade:
    """Trade model class.

    Args:
        stock_name (str): stock name.
        trade_type (TradeType): type of trade.
        quantity (float): stock quantity.
        price (float): paid price per stock.
        timestamp (float): timestamp of the trade.
    """

    def __init__(
        self,
        stock_name: str,
        trade_type: TradeType,
        quantity: float,
        price: float,
        timestamp: float = datetime.timestamp(datetime.utcnow()),
    ):
        # pylint: disable=too-many-arguments
        self.__stock_name = stock_name
        self.__type = trade_type
        self.__quantity = quantity
        self.__price = price
        self.__timestamp = timestamp

    def __repr__(self) -> str:
        """Get representation of a Trade object.

        Returns:
            str: representation of a Trade object.
        """
        return (
            f'<{self.__class__.__qualname__} "{self.__type.value}" of '
            f'Stock "{self.__stock_name}" object at {hex(id(self))}>'
        )

    @property
    def is_done_last_5_minutes(self) -> bool:
        """Check whether the trade has been done in the last 5 minutes.

        Returns:
            bool: whether the trade has been done in the last 5 minutes.
        """
        return (
            datetime.timestamp(datetime.utcnow()) - self.__timestamp <= 5 * 60
        )

    @property
    def quantity(self) -> float:
        """Get quantity.

        Returns:
            float: quantity.
        """
        return self.__quantity

    @property
    def price(self) -> float:
        """Get price.

        Returns:
            float: price.
        """
        return self.__price

    @property
    def type(self) -> TradeType:
        """Get type.

        Returns:
            TradeType: trade type.
        """
        return self.__type

    @property
    def timestamp(self) -> float:
        """Get timestamp.

        Returns:
            float: timestamp.
        """
        return self.__timestamp
