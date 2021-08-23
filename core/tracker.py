import json
from datetime import datetime
from json.encoder import JSONEncoder
from pathlib import Path

DATA_DIR = Path.home().joinpath(".tracker_api/trackers")


def object_hook(dct):
    if "date_str" in dct:
        return TrackerPoint(dct["date_str"], dct["value"])
    if "name" in dct:
        return Tracker(dct["name"], dct["points"])


class TrackerEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Tracker):
            return dict(name=o.name, points=o.points)
        elif isinstance(o, TrackerPoint):
            return dict(date_str=o.datetime.isoformat(), value=o.value)
        else:
            return json.JSONEncoder.default(self, o)


class TrackerPoint:
    def __init__(self, date_str: str, value: int) -> None:
        self.datetime = datetime.fromisoformat(date_str)
        self.value = value


class Tracker:
    def __init__(self, name: str, points: list[TrackerPoint]):
        self.name = name
        self.points = points

    def rename(self, name):
        """Rename the Tracker."""
        DATA_DIR.joinpath(f"{self.name}.json").rename(
            DATA_DIR.joinpath(f"{name}.json"))
        self.name = name
        self.save()

    def delete(self):
        """Delete the Tracker."""
        filepath = DATA_DIR.joinpath(f"{self.name}.json")
        filepath.unlink()

    def to_json(self):
        """Convert Tracker object to JSON."""
        return json.dumps(self, indent=4, cls=TrackerEncoder)

    def save(self):
        """Save the tracker to JSON."""
        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR.joinpath(f"{self.name}.json")
        filepath.touch(exist_ok=True)
        filepath.write_text(self.to_json())

    def modify_point(self, date_str: str, value: int):
        """Modify a point. Change its assigned value to the one given."""
        date_time = datetime.fromisoformat(date_str)
        for point in self.points:
            if point.datetime == date_time:
                point.value = value
                break
        self.save()

    def add_point(self, date_str: str, value: int):
        """Add a point to the tracker."""
        point = TrackerPoint(date_str, value)
        self.points.append(point)
        self.save()

    def delete_point(self, date_str: str):
        """Remove a point from the tracker."""
        date_time = datetime.fromisoformat(date_str)
        for point in self.points:
            if point.datetime == date_time:
                self.points.remove(point)
                break
        self.save()

    @classmethod
    def from_data(cls, name):
        """Load a tracker from the DATA_DIR."""
        filepath = DATA_DIR.joinpath(f"{name}.json")
        return cls.from_json(filepath.read_text())

    @staticmethod
    def from_json(json_str):
        """Load a tracker from a JSON string."""
        return json.loads(json_str, object_hook=object_hook)
