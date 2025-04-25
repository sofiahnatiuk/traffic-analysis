import argparse
from pathlib import Path
from src.save_data import save_all_data_to_csv
from src.analyze import get_busiest_stops
from src.report import create_combined_report

def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze and report on busiest public transport stops"
    )
    parser.add_argument("--map_top", type=int, default=250, help="Number of top busiest stops to include on the map")
    parser.add_argument("--chart_top", type=int, default=15, help="Number of top busiest stops to include in the chart")
    parser.add_argument("--eps", type=float, default=50.0, help="Clustering radius in meters for nearby stops")
    return parser.parse_args()

def main():
    args = parse_args()

    # Ensure folders exist
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    # Step 1: Save the data (fetch + parse)
    save_all_data_to_csv()

    # Step 2: Analyze
    busiest_stops = get_busiest_stops(
        "data/stops.csv",
        "data/intervals.csv",
        "reports/busiest_stops.csv",
        top_n=args.map_top,
        eps_meters=args.eps
    )

    # Step 3: Output
    print("Top Busiest Stops:")
    print(busiest_stops.to_string(index=False))
    create_combined_report(busiest_stops, chart_top_n=args.chart_top, map_top_n=args.map_top)

if __name__ == "__main__":
    main()
