from src.save_data import save_all_data_to_csv
from src.analyze import get_busiest_stops
from src.report import create_combined_report
from pathlib import Path

def main():
    """
    Main entry point for fetching, analyzing, and reporting public transport stop data.
    Steps:
    1. Fetch and save all data to CSV.
    2. Analyze the busiest stops based on vehicle frequency.
    3. Generate a combined HTML report with a chart and map.
    """

    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    # Step 1: Save the data (fetch + parse)

    save_all_data_to_csv()

    top_n = 250 # Max amount of busiest locations which will be in the output

    # Step 2: Analyze the data and print the results
    busiest_stops = get_busiest_stops("data/stops.csv", "data/intervals.csv", "reports/busiest_stops.csv", top_n, eps_meters=50)

    print("Top Busiest Stops:")
    print(busiest_stops.to_string(index=False))

    #Step 3: Generate a combined HTML report with top busiest stops chart and a map
    create_combined_report(busiest_stops, chart_top_n=15, map_top_n=top_n)

if __name__ == "__main__":
    main()
