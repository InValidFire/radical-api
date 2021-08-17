import sys

from target import Target
from fastapi import FastAPI, status
from response import Response

api = FastAPI()

api_data = {"version": "2021.8.4.0", "author": "Riley Housden"}


@api.post("/update")
def update():
    sys.exit(36)


@api.post("/restart")
def stop():
    sys.exit(26)


@api.get("/")
def quack():
    return "quack!"


@api.get("/target/points")
def list_points(name: str):
    try:
        target = Target.from_data(name)
        return Response(status.HTTP_200_OK, target.points)
    except FileNotFoundError:
        return Response(status.HTTP_204_NO_CONTENT, {})


@api.get("/target/points/add")
def add_point(name: str, datestr: str, value: int):
    try:
        target = Target.from_data(name)
    except FileNotFoundError:
        target = Target(name, [])
    target.add_point(datestr, value)
    return Response(status.HTTP_200_OK, target).to_json()


@api.put("/target/points/modify")
def modify_point(name: str, datestr: str, value: int):
    target = Target.from_data(name)
    target.modify_point(datestr, value)
    return 200


@api.delete("/target/points/delete")
def delete_point(name: str, datestr: str):
    target = Target.from_data(name)
    target.delete_point(datestr)
    return 200


@api.get("/target/rename")
def rename_target(name: str, new_name: str):
    target = Target.from_data(name)
    target.rename(new_name)
    return 200


@api.delete("/target/delete")
def delete_target(name: str):
    target = Target.from_data(name)
    target.delete()