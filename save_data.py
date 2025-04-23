# save_data.py

import csv
import logging
from fetch import TransportDataFetcher
from requests.exceptions import RequestException


def save_stops_to_csv(filename: str = "stops.csv") -> None:
    fetcher = TransportDataFetcher()
    routes = fetcher.parse_route_ids(fetcher.fetch_all_routes())

    # Set up logging
    logging.basicConfig(
        filename="save_stops_errors.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["route_id", "stop_id", "stop_name", "direction"])

        for route_id in routes:
            try:
                route_data = fetcher.fetch_route_detail(route_id)
                for direction in ("forward", "backward"):
                    for stop in route_data.get("stops", {}).get(direction, []):
                        stop_id = stop.get("i")
                        stop_name = stop.get("n")
                        if stop_id and stop_name:
                            writer.writerow([route_id, stop_id, stop_name, direction])
            except RequestException as e:
                logging.warning(f"Request failed for route_id {route_id}: {e}")
            except Exception as e:
                logging.warning(f"Unexpected error for route_id {route_id}: {e}")

    print(f"Saved data for {len(routes)} routes to {filename}")


if __name__ == "__main__":
    save_stops_to_csv()
