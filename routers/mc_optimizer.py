from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pathlib import Path
from datetime import datetime
from zipfile import ZipFile
import json

from starlette.responses import FileResponse


router = APIRouter(prefix="/mc_optimized")
ROOT_PATH = Path.home().joinpath(".radical_api/mc_optimized")
ROOT_PATH.mkdir(exist_ok=True)

class PackFile:
    def __init__(self, file: Path) -> None:
        self.file = file
        self.manifest = self.set_manifest()
        self.datetime = datetime.strptime(self.manifest['build-date'], "%d-%m-%Y-%H%M%S")
        self.build = self.manifest['build']

    def set_manifest(self):
        zf = ZipFile(self.file)
        return json.loads(zf.read("manifest.json").decode("utf-8"))

    def __lt__(self, other: PackFile):
        return self.datetime.__lt__(other.datetime)

def iterfile(path: Path):
        with path.open('rb') as fp:
            yield from fp

@router.get("/latest")
def latest_pack():
    files = []
    for file in ROOT_PATH.iterdir():
        files.append(PackFile(file))
    files.sort()
    if len(files) == 0:
        raise HTTPException(404, "No files found.")
    return FileResponse(files[-1].file, filename=f"mc-optimizer-pack-{files[-1].build}.zip")

@router.get("/build")
def get_build(build: int):
    for file in ROOT_PATH.iterdir():
        pf = PackFile(file)
        if pf.build == build:
            return FileResponse(pf.file, filename=f"mc-optimizer-pack-{pf.build}.zip")
    raise HTTPException(404, "Build not found.")

@router.get("/builds")
def get_builds():
    builds = []
    for file in ROOT_PATH.iterdir():
        pf = PackFile(file)
        builds.append(pf.manifest)
    return builds