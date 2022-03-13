from fastapi import Security, HTTPException, APIRouter, Depends
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from starlette.status import HTTP_403_FORBIDDEN

import logging
import uuid

from core.storage import Storage

router = APIRouter()
logger = logging.getLogger("security")
storage = Storage("security")

API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

try:
    system_key = storage.read_file("system_key.json")["system_key"]
except FileNotFoundError:
    logger.info("System Key not found, generating.")
    system_uuid = str(uuid.uuid4())
    storage.write_file("system_key.json", {"system_key": system_uuid})
    logger.info(f"System UUID: {system_uuid}")


def load_keys():
    return storage.read_file("api_keys.json")


def get_system_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie)
):
    system_key
    if api_key_query == system_key:
        return api_key_query
    elif api_key_header == system_key:
        return api_key_header
    elif api_key_cookie == system_key:
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
    keys: dict = storage.read_file("api_keys.json")
    new_key = str(uuid.uuid4())
    keys[new_key] = {}
    keys[new_key]["name"] = name
    storage.write_file("api_keys.json", keys)
    return new_key


@router.get("/key/me")
def key_info(access_token: APIKey = Depends(get_api_key)):
    data = load_keys()
    return data[access_token]
