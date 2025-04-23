import requests
from typing import Dict

class TransportFetcher:
    BASE_URL = "https://www.eway.in.ua/ajax/ua"
    ALL_ROUTES_PATH = "/lviv/routesPopup"
    ROUTE_DETAIL_PATH = "/lviv/routeInfo/{route_id}"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{BASE_URL}/network-map",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def fetch_all_routes(self) -> Dict:
        url = self.BASE_URL + self.ALL_ROUTES_PATH
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_route_detail(self, route_id: int) -> Dict:
        url = self.BASE_URL + self.ROUTE_DETAIL_PATH.format(route_id=route_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
