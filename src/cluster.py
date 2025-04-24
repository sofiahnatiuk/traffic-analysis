import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from math import radians

def cluster_busiest_stops(df: pd.DataFrame, eps_meters: float = 50.0) -> pd.DataFrame:
    """
    Groups nearby stops using DBSCAN and sums vehicles_per_week per cluster.
    """
    coords = np.radians(df[["latitude", "longitude"]].values)
    eps_rad = eps_meters / 6371000  # Earth radius in meters

    db = DBSCAN(eps=eps_rad, min_samples=1, algorithm="ball_tree", metric="haversine")
    df["cluster"] = db.fit_predict(coords)

    clustered = df.groupby("cluster").agg({
        "vehicles_per_week": "sum",
        "stop_name": lambda x: x.mode().iloc[0],  # most frequent name
        "latitude": "mean",
        "longitude": "mean"
    }).reset_index(drop=True)

    return clustered.sort_values(by="vehicles_per_week", ascending=False)
