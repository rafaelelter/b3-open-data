import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import logging
from io import BytesIO, StringIO
from typing import Iterable, Union, Any

import requests
import pandas as pd

from b3od.exceptions import RequestException
from b3od.utils import parse_date

logger = logging.getLogger(__name__)


class B3Scrapper:
    """Wrapper Class for downloading data from the B3 website"""

    SERVICE_DICT = {
        "TradeInformationConsolidated": "WebConsolidated",
        "OTCTradeInformationConsolidated": "WebConsolidated",
        "TradeInformationConsolidatedAfterHours": "WebConsolidated",
        "DerivativesOpenPosition": "WebConsolidated",
        "EconomicIndicatorPrice": "WebConsolidated",
        "InstrumentsConsolidated": "WebConsolidated",
        "OTCInstrumentsConsolidated": "WebConsolidated",
        "MarginScenarioLiquidAssets": "WebConsolidated",
        "LendingOpenPosition": "WebConsolidated",
        "LoanBalance": "WebConsolidated",
        "PositionLimits": "PositionLimits",
    }

    web_consolidated_base_url = "https://arquivos.b3.com.br/api"

    bmfbovespa_base_url = ""

    def __init__(self, session: requests.Session = None):
        self.session = session

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self) -> None:
        """Starts the scrapping session"""
        if self.session is None:
            self.session = requests.Session()

    def stop(self) -> None:
        """Stops the scrapping session"""
        if self.session is not None:
            self.session.close()

    def list_services(self):
        """List all available services"""
        return list(self.SERVICE_DICT.keys())

    def _basic_request(
        self, method: str, url: str, data: dict = None
    ) -> requests.Response:
        if self.session is None:
            self.start()

        if data is None:
            data = {}

        logger.debug("Sending '%s' request to '%s'", method, url)
        response = self.session.request(method, url, data=data)

        logger.debug("Response status code: %s", response.status_code)
        if response.status_code != 200:
            raise RequestException(response)

        logger.debug("Response content: %s", response.text[:100] + "...")
        return response

    def __download_web_consolidated(self, table: str, dt: Any) -> pd.DataFrame:
        """Downloads data from a table in B3 website for a given date"""

        dt = parse_date(dt)

        url = f"{self.web_consolidated_base_url}/download/requestname?fileName={table}&date={dt:%Y-%m-%d}&recaptchaToken="
        response = self._basic_request("get", url)

        redirect_url = response.json()["redirectUrl"].replace(
            "~", self.web_consolidated_base_url
        )
        response = self._basic_request("get", redirect_url)

        if response.text == "":
            logger.error("No data found for %s", dt)
            return pd.DataFrame()

        df = pd.read_csv(StringIO(response.text), sep=";", decimal=",")
        return df

    def __download_web_consolidated_many(
        self, table: str, dts: Iterable[Any]
    ) -> pd.DataFrame:
        """Multi-thread approach to download data from B3"""

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.__download_web_consolidated, table, dt)
                for dt in dts
            ]
            return pd.concat([f.result() for f in futures], ignore_index=True)

    def __download_position_limits(self, dt: date) -> pd.DataFrame:

        dt = parse_date(dt)
        url = f"https://bvmf.bmfbovespa.com.br/LimitesPosicoes/Posicoes/DownloadArquivoDiretorio?data={dt:%Y%m%d}"
        response = self._basic_request("get", url)

        df = pd.read_csv(
            BytesIO(base64.b64decode(response.text)), sep=";", decimal=","
        )
        return df

    def __download_position_limits_many(
        self, table: str, dts: Iterable[Any]
    ) -> pd.DataFrame:
        """Multi-thread approach to download data from B3"""

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.__download_position_limits, table, dt)
                for dt in dts
            ]
            return pd.concat([f.result() for f in futures], ignore_index=True)

    def download(self, table: str, dt: Union[Any, Iterable[Any]]) -> pd.DataFrame:
        """Downloads data from a table in B3 website for a given date (or set of dates)"""
        if not table in self.SERVICE_DICT:
            raise ValueError(f"Table must be one of {self.SERVICE_DICT.keys()}")
        service = self.SERVICE_DICT[table]

        if service == "WebConsolidated":
            if isinstance(dt, Iterable):
                return self.__download_web_consolidated_many(table, dt)
            return self.__download_web_consolidated(table, dt)
        if service == "PositionLimits":
            if isinstance(dt, Iterable):
                return self.__download_position_limits_many(table, dt)
            return self.__download_position_limits(dt)
        raise ValueError(f"Table must be one of {set(self.SERVICE_DICT.values())}")
