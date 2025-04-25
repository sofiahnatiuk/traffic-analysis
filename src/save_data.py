import logging
import pandas as pd
from src.fetch import TransportFetcher
from src.parse import TransportParser
from requests.exceptions import RequestException

def save_all_data_to_csv(
    stops_file: str = "data/stops.csv",
    intervals_file: str = "data/intervals.csv"
) -> None:
    """
    Saves fetched data to csv: stops.csv includes stops for every route
    and intervals.csv includes schedule-related info for routes
    """
    fetcher = TransportFetcher()
    parser = TransportParser()

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Log the start of the function
    logging.info("Starting to fetch and process transport data.")

    # Step 1: Fetch all routes and extract route IDs
    logging.info("Fetching all route data.")
    try:
        all_routes_data = fetcher.fetch_all_routes()
        route_ids = parser.parse_route_ids(all_routes_data)
        logging.info(f"Fetched {len(route_ids)} route IDs.")
    except RequestException as e:
        logging.error(f"Error fetching route data: {e}")
        return

    # Step 2: Fetch all route details in parallel
    logging.info(f"Fetching details for {len(route_ids)} routes in parallel.")
    route_details = {}
    try:
        route_details = fetcher.fetch_multiple_route_details(route_ids, max_workers=10)
        logging.info(f"Fetched details for {len(route_details)} routes.")
    except RequestException as e:
        logging.error(f"Error fetching route details: {e}")
        return

    stops = []
    intervals = []

    # Step 3: Parse stops and intervals from the fetched data
    logging.info("Parsing stops and intervals.")
    for route_id, route_data in route_details.items():
        try:
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
    logging.info(f"Saving {len(stops)} stops and {len(intervals)} intervals to CSV.")
    pd.DataFrame(stops).to_csv(stops_file, index=False)
    pd.DataFrame(intervals).to_csv(intervals_file, index=False)

    logging.info(f"Saved {len(stops)} stops to {stops_file} and {len(intervals)} intervals to {intervals_file}.")
    print(f"Saved {len(route_ids)} routes to {stops_file} and {intervals_file}.")

if __name__ == "__main__":
    save_all_data_to_csv()
