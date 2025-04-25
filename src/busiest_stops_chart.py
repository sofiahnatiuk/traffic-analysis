import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def save_busiest_stops_bar_chart(df: pd.DataFrame, image_path: str = "reports/bar_chart.png", chart_top_n: int = 15):
    df_top = df.sort_values("vehicles_per_week", ascending=False).head(chart_top_n)

    plt.figure(figsize=(12, 6))
    plt.barh(df_top["stop_name"], df_top["vehicles_per_week"], color="skyblue")
    plt.xlabel("Vehicles per Week")
    plt.title(f"Top Busiest Stops")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    Path(image_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(image_path)
    plt.close()

