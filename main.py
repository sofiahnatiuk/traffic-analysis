from save_data import save_all_data_to_csv
from analyze import get_busiest_stops
from map_locations import create_busiest_stops_map


def main():
    # Step 1: Save the data (fetch + parse)
    save_all_data_to_csv()

    top_n = 50 # Max amount of busiest locations which will be in the output

    # Step 2: Analyze the data and print the results
    busiest_stops = get_busiest_stops("stops.csv", "intervals.csv", "busiest_stops.csv", top_n)

    print("Top Busiest Stops:")
    print(busiest_stops.to_string(index=False))
    create_busiest_stops_map("busiest_stops.csv", top_n=top_n)

if __name__ == "__main__":
    main()
