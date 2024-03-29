import json
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from core.storage import Storage

storage = Storage("trackers")

def object_hook(dct):
    if "datetime" in dct:
        return TrackerPoint(dct["datetime"], dct["value"])
    if "date_str" in dct:  # old format
        return TrackerPoint(dct["date_str"], dct["value"])
    if "name" in dct:
        return Tracker(dct["name"], dct["points"])


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
        storage.rename_file(f"{self.name}.json", f"{name}.json")
        self.name = name
        storage.write_file(f"{self.name}.json", jsonable_encoder(self))

    def delete(self):
        """Delete the Tracker."""
        storage.delete_file(f"{self.name}.json")

    def modify_point(self, date_str: str, value: int):
        """Modify a point. Change its assigned value to the one given."""
        date_time = datetime.fromisoformat(date_str)
        for point in self.points:
            if point.datetime == date_time:
                point.value = value
                break
        storage.write_file(f"{self.name}.json", jsonable_encoder(self))

    def add_point(self, date_str: str, value: int):
        """Add a point to the tracker."""
        point = TrackerPoint(date_str, value)
        self.points.append(point)
        storage.write_file(f"{self.name}.json", jsonable_encoder(self))

    def delete_point(self, date_str: str):
        """Remove a point from the tracker."""
        date_time = datetime.fromisoformat(date_str)
        for point in self.points:
            if point.datetime == date_time:
                self.points.remove(point)
                break
        storage.write_file(f"{self.name}.json", jsonable_encoder(self))

    def list_points(self, start_date: datetime = None, end_date: datetime = None) -> list:
        """
        Return a list of all points that fall in-between the given start_date and end_date.

        :param start_date: the date the data returned should start at.
        If this is not given, it'll be a week from the given end_date.

        :param end_date: the date the data returned should end at. (included in output)
        If this is not given, it'll be today.

        :return: list of all points that fall in-between the given start_date and end_date.

        :raises ValueError: if either date parameter is set in the future, or if the end_date is before the start_date.
        """
        point_list = []
        if end_date is None:
            end_date = datetime.now().date()
        if start_date is None:
            start_date = (end_date - timedelta(days=7))  # assume we'll start a week prior to today.
        if end_date > datetime.now().date() or start_date > datetime.now().date() or end_date < start_date:
            raise ValueError(end_date)
        for point in self.points:
            if start_date <= point.datetime.date() <= end_date:
                point_list.append(point)
        return point_list

    @classmethod
    def from_data(cls, name):
        """Load a tracker from the DATA_DIR."""
        data = storage.read_file(f"{name}.json")
        return cls.from_json(data)

    @staticmethod
    def from_json(json_str):
        """Load a tracker from a JSON string."""
        return json.load(json_str, object_hook=object_hook)
