"""
Scrapping module for fetching data from B3's APIs.
"""

import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
import logging
from io import BytesIO, StringIO
from typing import Iterable, Union, Any

import requests
import pandas as pd
import numpy as np

from b3od.utils import parse_date, is_sequence
from b3od.meta import SERVICES_DTYPES, SERVICES_DATE_COLUMNS

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

    bmfbovespa_base_url = "https://bvmf.bmfbovespa.com.br"

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

    def __basic_request(self, method: str, url: str, **kwargs) -> requests.Response:
        if self.session is None:
            self.start()

        logger.debug("Sending '%s' request to '%s'", method, url)
        response = self.session.request(method, url, **kwargs)

        logger.debug("Response status code: %s", response.status_code)
        if response.status_code != 200:
            raise response.raise_for_status()

        logger.debug("Response content: %s", response.text[:100] + "...")
        return response

    def __download_web_consolidated(self, table: str, query_date: Any) -> pd.DataFrame:
        """Downloads data from a table in B3 website for a given date"""

        query_date = parse_date(query_date)

        url = f"{self.web_consolidated_base_url}/download/requestname"

        params = {
            "fileName": table,
            "date": query_date.strftime("%Y-%m-%d"),
            "recaptchaToken": "",
        }

        response = self.__basic_request("get", url, params=params)

        redirect_url = response.json()["redirectUrl"].replace(
            "~", self.web_consolidated_base_url
        )
        response = self.__basic_request("get", redirect_url)

        if response.text == "":
            logger.error("No data found for %s", query_date)
            return pd.DataFrame()

        queried_data = pd.read_csv(
            StringIO(response.text),
            sep=";",
            decimal=",",
            dtype=SERVICES_DTYPES[table],
            skiprows=1  # Remove header line ('Status do Arquivo: ...')
        )

        queried_data[SERVICES_DATE_COLUMNS[table]] = queried_data[
            SERVICES_DATE_COLUMNS[table]
        ].map(
            lambda x: datetime.strptime(x, "%Y-%m-%d").date()
            if not pd.isna(x)
            else np.nan,
        )

        return queried_data

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

    def __download_position_limits(self, query_date: date) -> pd.DataFrame:
        table = "PositionLimits"
        query_date = parse_date(query_date)
        url = f"{self.bmfbovespa_base_url}/LimitesPosicoes/Posicoes/DownloadArquivoDiretorio"

        params = {"data": query_date.strftime("%Y-%m-%d")}

        response = self.__basic_request("get", url, params=params)

        queried_data = pd.read_csv(
            BytesIO(base64.b64decode(response.text)),
            sep=";",
            decimal=",",
            dtype=SERVICES_DTYPES[table],
            parse_dates=SERVICES_DATE_COLUMNS[table],
            date_parser=(
                lambda x: datetime.strptime(x, "%Y-%m-%d").date()
                if not pd.isna(x)
                else np.nan
            ),
        )
        return queried_data

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

    def download(
        self, table: str, query_date: Union[Any, Iterable[Any]]
    ) -> pd.DataFrame:
        """Downloads data from a table in B3 website for a given date (or set of dates)"""
        if table not in self.SERVICE_DICT:
            raise ValueError(f"Table must be one of {self.SERVICE_DICT.keys()}")
        service = self.SERVICE_DICT[table]

        if service == "WebConsolidated":
            if is_sequence(query_date):
                logger.info("Downloading many")
                return self.__download_web_consolidated_many(table, query_date)
            logger.info("Downloading one")
            return self.__download_web_consolidated(table, query_date)
        if service == "PositionLimits":
            if is_sequence(query_date):
                return self.__download_position_limits_many(table, query_date)
            return self.__download_position_limits(query_date)
        raise ValueError(f"Table must be one of {set(self.SERVICE_DICT.values())}")
