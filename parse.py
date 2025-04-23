from typing import Dict, List, Tuple

class TransportParser:
    @staticmethod
    def parse_route_ids(data: Dict) -> List[int]:
        route_ids = set()
        for mode in ("bus_4", "tram_3", "trol_2"):
            for item in data.get(mode, []):
                route_ids.add(item[0])
        return sorted(route_ids)

    @staticmethod
    def parse_stops(route_data: Dict) -> List[Tuple[int, str, str]]:
        stops = []
        for direction in ("forward", "backward"):
            for stop in route_data.get("stops", {}).get(direction, []):
                stop_id = stop.get("i")
                stop_name = stop.get("n")
                if stop_id and stop_name:
                    stops.append((stop_id, stop_name, direction))
        return stops

    @staticmethod
    def parse_intervals(route_data: Dict) -> List[Tuple[str, str, int]]:
        intervals = []
        for day_pattern, ranges in route_data.get("intervals", {}).items():
            for entry in ranges:
                intervals.append((entry["from"], entry["to"], entry["i"]))
        return intervals
