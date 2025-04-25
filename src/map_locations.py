import pandas as pd
import folium
import branca.colormap as cm

def create_busiest_stops_map(df: pd.DataFrame) -> folium.Map:
    """
    Creates an interactive Folium map showing the busiest stops based on vehicle frequency.

    Args:
        df (pd.DataFrame): DataFrame with columns ['stop_name', 'latitude', 'longitude', 'vehicles_per_week']

    Returns:
        folium.Map: Interactive map object with color-scaled stop markers.
    """

    avg_lat = df["latitude"].mean()
    avg_lon = df["longitude"].mean()

    map_ = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    # Set up a color scale based on vehicles_per_week
    min_val = df["vehicles_per_week"].min()
    max_val = df["vehicles_per_week"].max()

    colormap = cm.linear.Dark2_03.scale(min_val, max_val)
    colormap.caption = "Vehicles per Week"

    # Add colored markers
    for _, row in df.iterrows():
        color = colormap(row["vehicles_per_week"])
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"{row['stop_name']} ({int(row['vehicles_per_week'])} vehicles/week)",
            tooltip=row["stop_name"]
        ).add_to(map_)

    # Add color scale legend to map
    colormap.add_to(map_)

    return map_
