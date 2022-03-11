import importlib
import logging
import platform

from pathlib import Path
from fastapi import FastAPI

logger = logging.getLogger("api")

api = FastAPI()
api_data = {"version": "2021.12.1.5", "author": "Riley Housden"}


def load_module(name: str):
    module = importlib.import_module(name)
    api.include_router(module.router)
    logger.info(f"Loaded module: {module.__name__}")


for m_path in Path("routers").glob("*"):
    if "__pycache__" in m_path.parts or "__init__" == m_path.stem:
        continue
    if platform.system() != "Windows":
        load_module(str(m_path).replace("/", ".").replace(".py", ""))
    else:
        load_module(str(m_path).replace("\\", ".").replace(".py", ""))


@api.get("/")
def quack():
    return api_data

if __name__ == "__main__":
    import uvicorn
    api_data["version"] += "-dev"
    uvicorn.run(api)