[![PyPI version](https://badge.fury.io/py/blp.svg)](https://badge.fury.io/py/blp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# About

b32u is a data extractor from Brazilian Stock Exchange (B3)

# Instalation

You can install from PyPI using  
```
pip install b32u
```

# Usage

```
from b32u.downloader import Downloader
from datetime import date, timedelta

dl = Downloader()
dl.start()
dt = date.today() - timedelta(days=1)
df = dl.get_data("TradeInformationConsolidated", dt)
```
