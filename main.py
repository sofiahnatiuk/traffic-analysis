from save_data import save_all_data_to_csv
from analyze import get_busiest_stops

def main():
    # Step 1: Save the data (fetch + parse)
    save_all_data_to_csv()

    top_n = 10 # Max amount of busiest locations which will be in the output

    # Step 2: Analyze the data and print the results
    busiest_stops = get_busiest_stops("stops.csv", "intervals.csv", top_n)

    print("Top 10 Busiest Stops:")
    print(busiest_stops.to_string(index=False))

if __name__ == "__main__":
    main()
