import logging
import pandas as pd
from fetch import TransportFetcher
from parse import TransportParser
from requests.exceptions import RequestException


def save_all_data_to_csv(
    stops_file: str = "stops.csv",
    intervals_file: str = "intervals.csv"
) -> None:
    fetcher = TransportFetcher()
    parser = TransportParser()

    logging.basicConfig(
        filename="save_errors.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    all_routes_data = fetcher.fetch_all_routes()
    route_ids = parser.parse_route_ids(all_routes_data)

    stops = []
    intervals = []

    for route_id in route_ids:
        try:
            route_data = fetcher.fetch_route_detail(route_id)

            for stop_id, stop_name, direction, latitude, longitude in parser.parse_stops(route_data):
                stops.append({
                    "route_id": route_id,
                    "stop_id": stop_id,
                    "stop_name": stop_name,
                    "direction": direction,
                    "latitude": latitude,
                    "longitude": longitude
                })

            for from_time, to_time, interval, weekdays in parser.parse_intervals(route_data):
                intervals.append({
                    "route_id": route_id,
                    "from": from_time,
                    "to": to_time,
                    "interval_sec": interval,
                    "weekdays": weekdays
                })

        except RequestException as e:
            logging.warning(f"Request failed for route_id {route_id}: {e}")
        except Exception as e:
            logging.warning(f"Unexpected error for route_id {route_id}: {e}")

    # Convert lists to DataFrames and write to CSV
    pd.DataFrame(stops).to_csv(stops_file, index=False)
    pd.DataFrame(intervals).to_csv(intervals_file, index=False)

    print(f"Saved {len(route_ids)} routes to {stops_file} and {intervals_file}.")


if __name__ == "__main__":
    save_all_data_to_csv()
