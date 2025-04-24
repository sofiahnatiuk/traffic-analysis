import logging
import pandas as pd
from src.fetch import TransportFetcher
from src.parse import TransportParser
from requests.exceptions import RequestException

def save_all_data_to_csv(
    stops_file: str = "data/stops.csv",
    intervals_file: str = "data/intervals.csv"
) -> None:
    fetcher = TransportFetcher()
    parser = TransportParser()

    logging.basicConfig(
        filename="save_errors.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Step 1: Fetch all routes and extract route IDs
    all_routes_data = fetcher.fetch_all_routes()
    route_ids = parser.parse_route_ids(all_routes_data)

    # Step 2: Fetch all route details in parallel
    route_details = fetcher.fetch_multiple_route_details(route_ids, max_workers=10)  # Parallel fetching

    stops = []
    intervals = []

    # Step 3: Parse stops and intervals from the fetched data
    for route_id, route_data in route_details.items():
        try:
            # Parse stops and intervals for this route
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

        except Exception as e:
            logging.warning(f"Error processing route_id {route_id}: {e}")

    # Step 4: Convert the parsed data to DataFrames and write to CSV
    pd.DataFrame(stops).to_csv(stops_file, index=False)
    pd.DataFrame(intervals).to_csv(intervals_file, index=False)

    print(f"Saved {len(route_ids)} routes to {stops_file} and {intervals_file}.")

if __name__ == "__main__":
    save_all_data_to_csv()
