import pandas as pd
import folium

def create_busiest_stops_map(stops_csv: str, output_html: str = "busiest_stops_map.html", top_n: int = 10):
    df = pd.read_csv(stops_csv)

    # Ensure we only take the top N based on vehicle traffic
    df_sorted = df.sort_values("vehicles_per_week", ascending=False).head(top_n)

    # Calculate map center
    avg_lat = df_sorted["latitude"].mean()
    avg_lon = df_sorted["longitude"].mean()

    # Create map
    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=14)

    # Add markers
    for _, row in df_sorted.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['stop_name']} ({int(row['vehicles_per_week'])} vehicles/day)",
            tooltip=row["stop_name"]
        ).add_to(map_)

    map_.save(output_html)
    print(f"Map saved to {output_html}")
