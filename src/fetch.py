import requests
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
logger = logging.getLogger(__name__)


class TransportFetcher:
    """
    Fetches transport route and stop data from the eway.in.ua.
    """
    BASE_URL = "https://www.eway.in.ua/ajax/ua/lviv"
    ALL_ROUTES_PATH = "/routesPopup"
    ROUTE_DETAIL_PATH = "/routeInfo/{route_id}"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{BASE_URL}",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def __enter__(self):
        """
        Allows TransportFetcher to be used in a `with` statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures that the session is closed when done.
        """
        self.session.close()

    def fetch_all_routes(self) -> Dict:
        """
        Fetches all route ids. Returns JSON-like data.
        """
        url = self.BASE_URL + self.ALL_ROUTES_PATH
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_route_detail(self, route_id: int) -> Dict:
        """
        Fetches detail about a specific route. Returns full route information,
        including all stops (id, name, coordinates), route schedule (working hours,
        interval between vehicles on route, week schedule).
        Returns JSON-like data.
        """
        url = self.BASE_URL + self.ROUTE_DETAIL_PATH.format(route_id=route_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_multiple_route_details(self, route_ids: List[int], max_workers: int = 10) -> Dict[int, Dict]:
        """
        Uses ThreadPoolExecutor for asynchronous data fetching- for multiple routes.
        """
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit each fetch_route_detail call as a separate task
            futures = {executor.submit(self.fetch_route_detail, rid): rid for rid in route_ids}
            for future in as_completed(futures):
                rid = futures[future]
                try:
                    # Get the result of the future (blocking until it's done)
                    data = future.result()
                    results[rid] = data
                except Exception as e:
                    logger.warning(f"Failed to fetch route {rid}: {e}")
        return results
