import requests
from typing import Dict, Any
from tenacity import retry, stop_after_attempt


class ThirdPartyAPI:
    @retry(stop=stop_after_attempt(10))
    def call_api(self, url: str, headers: Dict[str, Any] = None, timeout: int = 5):
        if headers is None:
            headers = {}
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()
        return response.json()


third_party_api = ThirdPartyAPI()
