import pandas as pd
import matplotlib.pyplot as plt

def save_busiest_stops_bar_chart(df: pd.DataFrame, image_path: str = "reports/bar_chart.png", top_n: int = 15):
    df_top = df.sort_values("vehicles_per_week", ascending=False).head(top_n)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    plt.barh(df_top["stop_name"], df_top["vehicles_per_week"], color="skyblue")
    plt.xlabel("Vehicles per Week")
    plt.title(f"Top {top_n} Busiest Stops")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

