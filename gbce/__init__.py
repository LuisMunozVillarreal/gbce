"""Global Beverage Corporation Exchange package."""


__author__ = "Luis Munoz Villarreal"
__email__ = "luis.munoz.villarreal@gmail.com"
__version__ = "0.1"

import logging
from typing import Union

from .logger import LoggerMixin
from .models.stock import Stock, StockType
from .models.stock.common import CommonStock
from .models.stock.preferred import PreferredStock


class Gbce(LoggerMixin):
    """Global Beverage Corporation Exchange class.

    Args:
        logger_level (int): logger level
    """

    __stocks: dict[str, Union[PreferredStock, CommonStock]]

    def __init__(self, logger_level: int = logging.INFO):
        super().__init__(logger_level)
        self.__logger_level = logger_level
        self.__stocks = {}

    def add_stock(
        self,
        name: str,
        stock_type: StockType,
        last_dividend: float,
        fixed_dividend: float,
        par_value: float,
    ) -> Union[Stock, None]:
        """Add a stock.

        Args:
            name (str): stock name.
            stock_type (str): stock type.
            last_dividend (float): stock last dividend.
            fixed_dividend (float): stock fixed dividend.
            par_value (float): stock par value.

        Returns:
            Stock: added stock.
            None: if there is already a stock with that name.
        """
        # pylint: disable=too-many-arguments

        if name in self.__stocks:
            self._log.warning("Stock with name %s already exists.", name)
            return None

        values = {
            "name": name,
            "last_dividend": last_dividend,
            "fixed_dividend": fixed_dividend,
            "par_value": par_value,
            "logger_level": self.__logger_level,
        }

        if stock_type == StockType.COMMON:
            self.__stocks[name] = CommonStock(**values)  # type: ignore
        elif stock_type == StockType.PREFERRED:
            self.__stocks[name] = PreferredStock(**values)  # type: ignore
        else:
            self._log.warning("Unknown stock type %s.", stock_type)
            return None

        return self.__stocks[name]

    @property
    def stocks(self) -> dict[str, Union[PreferredStock, CommonStock]]:
        """Get stocks.

        Returns:
            dict[str, Union[PreferredStock, CommonStock]]: GBCE stocks.
        """
        return self.__stocks

    def calculate_all_share_index(self) -> float:
        """Calculate all share index.

        Returns:
            float: share index.
        """
        index = len(self.__stocks)
        vwsp = 1.0
        for stock in self.__stocks.values():
            vwsp *= stock.calculate_volume_weighted_stock_price()
        return vwsp ** (1 / index)
