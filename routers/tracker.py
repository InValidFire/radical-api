from datetime import datetime
from functools import wraps

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from .security import get_api_key
from core.tracker import Tracker

router = APIRouter()


def check_name(router_fn):
    @wraps(router_fn)
    def _check_name_fn(name: str, *args, **kwargs):
        name += f"-{kwargs['access_token']}"
        return router_fn(name, *args, **kwargs)
    return _check_name_fn


@router.get("/tracker/points")
@check_name
def list_points(name: str, start_date=None, end_date=None, access_token: APIKey = Depends(get_api_key)):
    if start_date is not None:
        start_date = datetime.fromisoformat(start_date)
    if end_date is not None:
        end_date = datetime.fromisoformat(end_date)
    try:
        tracker = Tracker.from_data(name)
        return tracker.list_points(start_date, end_date)
    except FileNotFoundError:
        return {}


@router.get("/tracker/points/add")
@check_name
def add_point(name: str, value: int, date_str: str = None, access_token: APIKey = Depends(get_api_key)):
    if date_str is None:
        date_str = datetime.now().isoformat()
    try:
        tracker = Tracker.from_data(name)
    except FileNotFoundError:
        tracker = Tracker(name, [])
    tracker.add_point(date_str, value)
    return tracker.list_points()


@router.put("/tracker/points/modify")
@check_name
def modify_point(name: str, date_str: str, value: int, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.modify_point(date_str, value)
    return 200


@router.delete("/tracker/points/delete")
@check_name
def delete_point(name: str, date_str: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.delete_point(date_str)
    return 200


@router.get("/tracker/rename")
@check_name
def rename_tracker(name: str, new_name: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.rename(new_name)
    return 200


@router.delete("/tracker/delete")
@check_name
def delete_tracker(name: str, access_token: APIKey = Depends(get_api_key)):
    tracker = Tracker.from_data(name)
    tracker.delete()
