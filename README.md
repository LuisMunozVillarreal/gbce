# JP Morgan assessment

This assessment has been developed using python 3.10.5 and Debian 12.

## Installation

`pip` version 22 or higher is required.

In order to install the package to use its functionality, execute the following
command:

    pip install --user git+https://github.com/LuisMunozVillarreal/gbce.git

## Usage

Please, find below examples of how to use this package:

### Instantiate the exchange

```
>>> from gbce import Gbce
>>> gbce = Gbce()
```

### Add stocks

```
>>> gbce.stocks
{}
>>> from gbce.models.stock import StockType
>>> gbce.add_stock("TEA", StockType.COMMON, 0, None, 100)
<CommonStock "TEA" object at 0x7f92619f9120>
>>> gbce.add_stock("GIN", StockType.PREFERRED, 8, 2, 100)
<PreferredStock "GIN" object at 0x7f9261c6e380>
>>> gbce.stocks
{'TEA': <CommonStock "TEA" object at 0x7f92619f9120>, 'GIN': <PreferredStock "GIN" object at 0x7f9261c6e380>}
```

### Make some calculations

```
>>> tea = gbce.stocks.get("TEA")
>>> tea.calculate_dividend_yield(10.5)
0.0
>>> gin = gbce.stocks.get("GIN")
>>> gin.calculate_dividend_yield(5.6)
35.714285714285715
>>> gin.calculate_p_e_ratio(5.6)
0.7
```

### Trade

```
>>> tea.buy(10, 100)
<Trade "Buy" of "TEA" object at 0x7f00d8fdd930>
>>> tea.sell(5, 200)
<Trade "Sell" of "TEA" object at 0x7f00d91b1f90>
>>> tea.trades
[<Trade "Buy" of Stock "TEA" object at 0x7f00d8fdd930>, <Trade "Sell" of Stock "TEA" object at 0x7f00d91b1f90>]
>>> gin.buy(100, 300)
<Trade "Buy" of "GIN" object at 0x7f00d91b2020>
>>> gin.sell(50, 200)
<Trade "Sell" of "GIN" object at 0x7f00d91b2080>
>>> gin.trades
[<Trade "Buy" of Stock "GIN" object at 0x7f00d91b2020>, <Trade "Sell" of Stock "GIN" object at 0x7f00d91b2080>]
```

### Record pre-existing trades

```
>>> from gbce.models.trade import TradeType
>>> tea.record_trade(TradeType.BUY, 40, 90, 1000000000)
<Trade "Buy" of Stock "TEA" object at 0x7ff961fcdf30>
>>> gin.record_trade(TradeType.SELL, 70, 180, 1000000000)
<Trade "Sell" of Stock "GIN" object at 0x7ff961fcd1e0>
```

### Calculate GBCE all share index

```
>>> gbce.calculate_all_share_index()
188.56180831641268
```

## Production quality assurance

This package uses the following QA tools to assure a production quality for the
package:
1. `pytest`
1. `flake8`
1. `black`
1. `mypy`
1. `pylint`
1. `pydocstyle`

In order to run these QA tools against this package, run the following
commands:

Clone the repository:

    git clone git@github.com:LuisMunozVillarreal/gbce.git

Change directory:

    cd gbce
    
Run `tox`:

    tox

`tox` will install the package in a virtual environment and execute all the
necessary checks.
