from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from .security import get_api_key
from core.tracker import Tracker

router = APIRouter()


@router.get("/tracker/points")
def list_points(name: str, access_token: APIKey = Depends(get_api_key)):
    try:
        tracker = Tracker.from_data(name)
        return tracker.points
    except FileNotFoundError:
        return {}


@router.get("/tracker/points/add")
def add_point(name: str, value: int, date_str: str = None, access_token: APIKey = Depends(get_api_key)):
    if date_str is None:
        date_str = datetime.now().isoformat()
    try:
        tracker = Tracker.from_data(name)
    except FileNotFoundError:
        tracker = Tracker(name, [])
    tracker.add_point(date_str, value)
    return tracker.to_json()


@router.put("/tracker/points/modify")
def modify_point(name: str, date_str: str, value: int, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.modify_point(date_str, value)
    return 200


@router.delete("/tracker/points/delete")
def delete_point(name: str, date_str: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.delete_point(date_str)
    return 200


@router.get("/tracker/rename")
def rename_tracker(name: str, new_name: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.rename(new_name)
    return 200


@router.delete("/tracker/delete")
def delete_tracker(name: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.delete()