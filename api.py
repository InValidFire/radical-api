import importlib
import logging

from pathlib import Path
from fastapi import FastAPI

logger = logging.getLogger("api")

api = FastAPI()
api_data = {"version": "2021.8.23.0", "author": "Riley Housden"}


def load_module(name: str):
    module = importlib.import_module(name)
    api.include_router(module.router)
    logger.info(f"Loaded module: {module.__name__}")


for m_path in Path("routers").glob("*"):
    if "__pycache__" in m_path.parts or "__init__" == m_path.stem:
        continue
    load_module(str(m_path).replace("/", ".").replace(".py", ""))


@api.get("/")
def quack():
    return api_data
