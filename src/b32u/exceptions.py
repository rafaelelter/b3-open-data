import requests


class RequestException(Exception):
    """Raised when a request fails."""

    def __init__(self, response: requests.Response, explanation: str = ""):
        self.url = response.url
        self.status_code = response.status_code
        self.reason = response.reason
        self.explaination = explanation

    def __str__(self):
        return f"{self.explaination} returned code {self.status_code} {self.reason} for {self.url}"
