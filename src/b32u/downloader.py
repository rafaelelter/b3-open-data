from datetime import date
import logging
from io import StringIO
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor

import requests
import pandas as pd

from b32u.exceptions import RequestException
from b32u.utils import parse_date

logger = logging.getLogger(__name__)

TABLES = [
    "TradeInformationConsolidated",
    "OTCTradeInformationConsolidated",
    "TradeInformationConsolidatedAfterHours",
    "DerivativesOpenPosition",
    "EconomicIndicatorPrice",
    "InstrumentsConsolidated",
    "OTCInstrumentsConsolidated",
    "MarginScenarioLiquidAssets",
    "LendingOpenPosition",
    "LoanBalance",
]


class Downloader:
    """Wrapper Class for downloading data from the B3 website"""

    base_url = "https://arquivos.b3.com.br/api"

    def __init__(self, session: requests.Session = None):
        self.session = session

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def start(self) -> None:
        if self.session is None:
            self.session = requests.Session()

    def stop(self) -> None:
        if self.session is not None:
            self.session.close()

    def _basic_request(
        self, method: str, url: str, data: dict = None
    ) -> requests.Response:
        if self.session is None:
            self.start()

        if data is None:
            data = {}

        url = url.replace("~", self.base_url)

        logger.debug("Sending '%s' request to '%s'", method, url)
        response = self.session.request(method, url, data=data)

        logger.debug("Response status code: %s", response.status_code)
        if response.status_code != 200:
            raise RequestException(response)

        logger.debug("Response content: %s", response.text[:100] + "...")
        return response

    def get_data(self, table: str, dt: date) -> pd.DataFrame:
        """Downloads data from a table in B3 website for a given date"""

        if not table in TABLES:
            raise ValueError(f"Table must be one of {TABLES}")

        dt = parse_date(dt)

        url = f"{self.base_url}/download/requestname?fileName={table}&date={dt:%Y-%m-%d}&recaptchaToken="
        response = self._basic_request("get", url)

        redirect_url = response.json()["redirectUrl"]
        response = self._basic_request("get", redirect_url)

        if response.text == "":
            logger.error("No data found for %s", dt)
            return pd.DataFrame()

        df = pd.read_csv(StringIO(response.text), sep=";", decimal=",")
        return df

    def get_data_multiple_days(self, table: str, dts: Iterable[date]) -> pd.DataFrame:
        """Multi-thread approach to download data from B3"""

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_data, table, parse_date(dt)) for dt in dts
            ]
            return pd.concat([f.result() for f in futures])
