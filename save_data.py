import csv
import logging
from fetch import TransportFetcher
from parse import TransportParser
from requests.exceptions import RequestException


def save_all_data_to_csv(
    stops_file: str = "stops.csv",
    intervals_file: str = "intervals.csv"
) -> None:
    fetcher = TransportFetcher()
    parser = TransportParser()

    # Set up logging
    logging.basicConfig(
        filename="save_errors.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    all_routes_data = fetcher.fetch_all_routes()
    route_ids = parser.parse_route_ids(all_routes_data)

    with open(stops_file, mode="w", newline="", encoding="utf-8") as sf, \
         open(intervals_file, mode="w", newline="", encoding="utf-8") as inf:

        stop_writer = csv.writer(sf)
        interval_writer = csv.writer(inf)

        stop_writer.writerow(["route_id", "stop_id", "stop_name", "direction"])
        interval_writer.writerow(["route_id", "from", "to", "interval_sec"])

        for route_id in route_ids:
            try:
                route_data = fetcher.fetch_route_detail(route_id)

                for stop_id, stop_name, direction in parser.parse_stops(route_data):
                    stop_writer.writerow([route_id, stop_id, stop_name, direction])

                for from_time, to_time, interval in parser.parse_intervals(route_data):
                    interval_writer.writerow([route_id, from_time, to_time, interval])

            except RequestException as e:
                logging.warning(f"Request failed for route_id {route_id}: {e}")
            except Exception as e:
                logging.warning(f"Unexpected error for route_id {route_id}: {e}")

    print(f"Saved {len(route_ids)} routes to {stops_file} and {intervals_file}.")


if __name__ == "__main__":
    save_all_data_to_csv()
