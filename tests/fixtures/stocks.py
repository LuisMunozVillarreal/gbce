"""Stock fixtures for testing."""

from gbce.models.stock import StockType

SAMPLE_STOCKS = {
    "TEA": {
        "type": StockType.COMMON,
        "last_dividend": 0,
        "fixed_dividend": None,
        "par_value": 100,
    },
    "POP": {
        "type": StockType.COMMON,
        "last_dividend": 8,
        "fixed_dividend": None,
        "par_value": 100,
    },
    "ALE": {
        "type": StockType.COMMON,
        "last_dividend": 23,
        "fixed_dividend": None,
        "par_value": 60,
    },
    "GIN": {
        "type": StockType.PREFERRED,
        "last_dividend": 8,
        "fixed_dividend": 2,
        "par_value": 100,
    },
    "JOE": {
        "type": StockType.COMMON,
        "last_dividend": 13,
        "fixed_dividend": None,
        "par_value": 250,
    },
}
