"""Common Stock module."""


from . import Stock


class CommonStock(Stock):
    """Common Stock class.

    Specialised class for common stock.
    """

    def _calculate_dividend_yield(self, price: float) -> float:
        """Calculate the dividend yield of the stock.

        Args:
            price (float): common stock price.

        Returns:
            float: dividend yield percentage.
        """
        return self._last_dividend / price * 100
