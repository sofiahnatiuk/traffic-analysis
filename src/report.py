from pathlib import Path
from src.map_locations import create_busiest_stops_map
from src.busiest_stops_chart import save_busiest_stops_bar_chart
import pandas as pd

def create_combined_report(
    full_df: pd.DataFrame,
    output_html: str = "reports/combined_report.html",
    chart_top_n: int = 15,
    map_top_n: int = 50
):
    """
    Creates a combined HTML report showing:
    - A bar chart of the top N busiest stops.
    - An interactive map of the top N busiest stops.

    Args:
        full_df (pd.DataFrame): DataFrame with stop data including 'vehicles_per_week'.
        output_html (str): Path to save the final report.
        chart_top_n (int): Number of stops to include in bar chart.
        map_top_n (int): Number of stops to include in map.

    Returns:
        None
    """

    chart_df = full_df.sort_values("vehicles_per_week", ascending=False).head(chart_top_n)
    map_df = full_df.sort_values("vehicles_per_week", ascending=False).head(map_top_n)

    # Save bar chart
    save_busiest_stops_bar_chart(chart_df)

    # Create and save map as a standalone file
    map_ = create_busiest_stops_map(map_df)
    map_path = "reports/map.html"
    Path(map_path).parent.mkdir(parents=True, exist_ok=True)
    map_.save(map_path)

    map_html_iframe = f'<iframe src="{Path(map_path).name}" width="90%" height="600px" frameborder="0"></iframe>'

    # Combine into final HTML
    html = f"""
    <html>
    <head>
        <title>Busiest Stops Report</title>
        <style>
            body {{
                font-family: sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            img {{
                max-width: 70%;
                height: auto;
                margin-top: 20px;
            }}
            .map-container {{
                width: 90%;
                height: 600px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Busiest Public Transport Stops</h1>
        <img src="bar_chart.png" alt="Busiest Stops Bar Chart">
        <div class="map-container">
            {map_html_iframe}
        </div>
    </body>
    </html>
    """

    Path(output_html).write_text(html)
    print(f"Report saved as {output_html}")
