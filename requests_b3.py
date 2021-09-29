from typing import Generator
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm
from datetime import date

class RequestsB3:
    
    def __init__(self):
        self.base_url = "https://arquivos.b3.com.br/tabelas/table"

    def _get_request(self, page:int)->requests.Response:
        with requests.session() as session:
            retry = Retry(connect=5, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session.get(self.working_url + '/' + str(page))

    def _request_values(self)->Generator:
        page = 1
        err_count = 0

        response = self._get_request(1)
        assert response.status_code == 200, "Erro no request."
        data = response.json()
        max_pages = data["pageCount"]

        for page in tqdm(range(1,max_pages+1)):
            response = self._get_request(page)
            assert response.status_code == 200, "Erro no request."

            if not 'application/json' in response.headers.get('Content-Type'):
                err_count += 1
                if err_count < 5:
                    continue
                else:
                    print("Muitos erros ocorreram na importação. Request finalizado antecipadamente")
                    break
            
            data = response.json()

            if data["pageCount"] <= 0:
                break
            else:
                yield data["values"]
                page += 1
                err_count = 0

    def _request_columns(self)->tuple:
        response = self._get_request(1)
        data = response.json()
        return tuple(col["name"] for col in data["columns"])

    def request_data(self, table:str, dt:date)->dict:
        self.working_url = f'{self.base_url}/{table}/{dt}'
        values = tuple(tuple(item) for sublist in self._request_values() for item in sublist)
        columns = self._request_columns()
        return {"columns": columns, "data": values}

    def request_economic_indicator(self, dt:date):
        return self.request_data(table="EconomicIndicatorPrice", dt=dt)
    
    def request_trade_information(self, dt:date):
        return self.request_data(table="TradeInformationConsolidated", dt=dt)
    
    def request_instruments(self, dt:date):
        return self.request_data(table="InstrumentsConsolidated", dt=dt)

    