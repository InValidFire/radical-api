from fastapi import Security, HTTPException, APIRouter, Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from starlette.status import HTTP_403_FORBIDDEN

from pathlib import Path
import logging
import uuid
import json

router = APIRouter()
logger = logging.getLogger("security")
ROOT_PATH = Path.home().joinpath(".tracker_api/keys")

API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

system_key_path = ROOT_PATH.joinpath("system_key")
if not system_key_path.exists():
    logger.info("System Key not found, generating.")
    system_key_path.parent.mkdir(parents=True, exist_ok=True)
    system_key_path.touch()
    system_uuid = str(uuid.uuid4())
    system_key_path.write_text(system_uuid)
    logger.info(f"System UUID: {system_uuid}")


def load_keys():
    path = ROOT_PATH.joinpath("api_keys.json")
    if not path.exists():
        path.touch()
        path.write_text("{}")
    with path.open("r") as f:
        data = json.load(f)
    return data


def get_system_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie)
):
    path = ROOT_PATH.joinpath("system_key")
    if api_key_query == path.read_text():
        return api_key_query
    elif api_key_header == path.read_text():
        return api_key_header
    elif api_key_cookie == path.read_text():
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie)
):
    if api_key_query in load_keys():
        return api_key_query
    elif api_key_header in load_keys():
        return api_key_header
    elif api_key_cookie in load_keys():
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


@router.get("/key/create")
def create_key(name, system_key: APIKey = Depends(get_system_key)):
    keys: dict = load_keys()
    new_key = str(uuid.uuid4())
    keys[new_key] = {}
    keys[new_key]["name"] = name
    path = ROOT_PATH.joinpath("api_keys.json")
    with path.open("w") as f:
        json.dump(keys, f, indent=4, sort_keys=True)
    return new_key


@router.get("/key/me")
def key_info(api_key: APIKey = Depends(get_api_key)):
    data = load_keys()
    return data[api_key]
