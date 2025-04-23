import pandas as pd

class RouteDataLoader:
    """
    Loads and prepares data from CSV files.
    """

    def __init__(self, stops_csv: str, intervals_csv: str) -> None:
        self.stops_df = pd.read_csv(stops_csv)
        self.intervals_df = pd.read_csv(intervals_csv)

    def get_dataframes(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return self.stops_df, self.intervals_df


class StopAnalyzer:
    """
    Analyzes stop activity based on route intervals and weekday weights.
    """

    def __init__(self, stops_df: pd.DataFrame, intervals_df: pd.DataFrame) -> None:
        self.stops_df = stops_df
        self.intervals_df = intervals_df

    def _get_weekday_weight(self, weekdays: str) -> int:
        """
        Calculate the number of days the transport runs based on the weekday mask.
        """
        weekdays_str = str(weekdays)  # Ensure it's a string
        return weekdays_str.count('1')

    def estimate_vehicles_per_day(self) -> pd.DataFrame:
        """
        Estimates number of vehicles per route per day using interval data,
        incorporating weekday weights.
        Returns a DataFrame with 'route_id' and 'adjusted_vehicles_per_day'.
        """
        df = self.intervals_df.copy()

        # Convert time columns to timedelta and compute operating minutes
        df["from_minutes"] = pd.to_timedelta(df["from"]).dt.total_seconds() / 60
        df["to_minutes"] = pd.to_timedelta(df["to"]).dt.total_seconds() / 60
        df["operating_minutes"] = df["to_minutes"] - df["from_minutes"]

        # Calculate basic vehicles per day (no weekday weighting yet)
        df["vehicles_per_day"] = (df["operating_minutes"] / df["interval_sec"]) * 60

        # Include weekday mask in the dataframe (e.g., '1111100' for Mon-Fri)
        df["weekday_mask"] = df["weekdays"]  # assuming there's a column 'weekdays' with a string like '1111100'
        df["weekday_weight"] = df["weekday_mask"].apply(self._get_weekday_weight)

        # Now apply the weekday weight to the vehicles per day estimate
        df["adjusted_vehicles_per_day"] = df["vehicles_per_day"] * df["weekday_weight"]

        # Group by route and calculate the average adjusted vehicles per day
        result = df.groupby("route_id")["adjusted_vehicles_per_day"].mean().reset_index()
        return result

    def compute_busiest_stops(self) -> pd.DataFrame:
        """
        Combines stops with vehicle frequency and ranks busiest stops.
        """
        vehicles_df = self.estimate_vehicles_per_day()
        merged = pd.merge(self.stops_df, vehicles_df, on="route_id", how="left")

        stop_coords = self.stops_df[["stop_id", "latitude", "longitude"]].drop_duplicates(subset="stop_id")

        # Aggregate by stop and compute total vehicles per stop
        stop_stats = merged.groupby(["stop_id", "stop_name"])[
            "adjusted_vehicles_per_day"
        ].sum().reset_index()

        # Join coordinates back in
        stop_stats = pd.merge(stop_stats, stop_coords, on="stop_id", how="left")
        return stop_stats.sort_values(by="adjusted_vehicles_per_day", ascending=False)


def get_busiest_stops(stops_file: str, intervals_file: str, output_csv: str = "busiest_stops.csv", top_n: int = 10) -> pd.DataFrame:
    loader = RouteDataLoader(stops_file, intervals_file)
    stops_df, intervals_df = loader.get_dataframes()

    analyzer = StopAnalyzer(stops_df, intervals_df)
    busiest = analyzer.compute_busiest_stops()

    busiest.head(top_n).to_csv(output_csv, index=False)
    print(f"Saved top {top_n} busiest stops to {output_csv}")
    return busiest.head(top_n)
