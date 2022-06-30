"""Preferred Stock module."""


from . import Stock


class PreferredStock(Stock):
    """Preferred Stock class.

    Specialised class for preferred stock.
    """

    def _calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield of the stock.

        Args:
            price (float): preferred stock price.

        Returns:
            float: dividend yield percentage.
        """
        return self._fixed_dividend / 100 * self._par_value / price * 100
