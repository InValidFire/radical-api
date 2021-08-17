import json
from datetime import datetime
from json.encoder import JSONEncoder
from pathlib import Path

DATA_DIR = Path.home().joinpath(".targetdata")


class TargetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%m/%d/%Y - %H:%M")
        else:
            return o.__dict__


class TargetPoint:
    def __init__(self, datestr: str, value: int) -> None:
        self.datetime = datetime.strptime(datestr, "%m/%d/%Y - %H:%M")
        self.value = value


class Target:
    def __init__(self, name: str, points: list[TargetPoint]):
        self.name = name
        self.points = points

    def rename(self, name):
        """Rename the Target."""
        DATA_DIR.joinpath(f"{self.name}.json").rename(
            DATA_DIR.joinpath(f"{name}.json"))
        self.name = name
        self.save()

    def delete(self):
        """Delete the Target."""
        filepath = DATA_DIR.joinpath(f"{self.name}.json")
        filepath.unlink()

    def to_json(self):
        """Convert Target object to JSON."""
        return json.dumps(self, indent=4, cls=TargetEncoder)

    def save(self):
        """Save the tracker to JSON."""
        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR.joinpath(f"{self.name}.json")
        filepath.touch(exist_ok=True)
        filepath.write_text(self.to_json())

    def modify_point(self, datestr: str, value: int):
        """Modify a point. Change its assigned value to the one given."""
        date_time = datetime.strptime(datestr, "%m/%d/%Y - %H:%M")
        for point in self.points:
            if point.datetime == date_time:
                point.value = value
                break
        self.save()

    def add_point(self, datestr: str, value: int):
        """Add a point to the tracker."""
        point = TargetPoint(datestr, value)
        self.points.append(point)
        self.save()

    def delete_point(self, datestr: str):
        """Remove a point from the tracker."""
        date_time = datetime.strptime(datestr, "%m/%d/%Y - %H:%M")
        for point in self.points:
            if point.datetime == date_time:
                self.points.remove(point)
                break
        self.save()

    @classmethod
    def from_data(cls, name):
        """Load a target from the DATA_DIR."""
        filepath = DATA_DIR.joinpath(f"{name}.json")
        return cls.from_json(filepath.read_text())

    @classmethod
    def from_json(cls, json_str):
        """Load a target from a JSON string."""
        obj = json.loads(json_str)
        return cls(obj['name'], obj['points'])
