# fetch.py

import requests
from typing import Dict, List, Tuple


class TransportDataFetcher:
    """
    A client for fetching public transport data from eway.in.ua.
    """

    BASE_URL = "https://www.eway.in.ua/ajax"
    ALL_ROUTES_PATH = "/ua/lviv/routesPopup"
    ROUTE_DETAIL_PATH = "/lviv/routeScheme/{route_id}"

    DEFAULT_HEADERS = {
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
        self.session.headers.update(self.DEFAULT_HEADERS)

    def fetch_all_routes(self) -> Dict:
        """
        Fetch the list of all routes, grouped by transport mode.
        """
        url = self.BASE_URL + self.ALL_ROUTES_PATH
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def parse_route_ids(self, data: Dict) -> List[int]:
        """
        Extract all unique route IDs from the JSON response.
        """
        route_ids = set()
        for mode in ("bus_4", "tram_3", "trol_2"):
            mode_data = data.get(mode, {})
            for item in mode_data:
                route_id = item[0]  # first element is route ID
                route_ids.add(route_id)
        return sorted(route_ids)

    def fetch_route_detail(self, route_id: int) -> Dict:
        """
        Fetch detailed information for a specific route by ID.
        """
        url = self.BASE_URL + self.ROUTE_DETAIL_PATH.format(route_id=route_id)
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def parse_stops_from_route(self, route_data: Dict) -> List[Tuple[int, str]]:
        """
        Extract stop IDs and names from both directions of a route.
        """
        stops = []
        stops_section = route_data.get("stops", {})

        for direction in ("forward", "backward"):
            for stop in stops_section.get(direction, []):
                stop_id = stop.get("i")
                stop_name = stop.get("n")
                if stop_id is not None and stop_name is not None:
                    stops.append((stop_id, stop_name))

        return stops


def main():
    fetcher = TransportDataFetcher()

    print("Fetching all routes...")
    all_routes_data = fetcher.fetch_all_routes()
    route_ids = fetcher.parse_route_ids(all_routes_data)

    print(f"Found {len(route_ids)} routes.\n")

    for route_id in route_ids:
        detail = fetcher.fetch_route_detail(route_id)
        stops = fetcher.parse_stops_from_route(detail)
        print(f"Route {route_id}:")
        for stop_id, stop_name in stops:
            print(f"  - {stop_id}: {stop_name}")


if __name__ == "__main__":
    main()
