import logging
from pathlib import Path

import pywizlight
from pywizlight.scenes import get_id_from_scene_name

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from .security import get_api_key

logger = logging.getLogger("lights")
router = APIRouter(prefix="/lights", tags=["lights"])

# TODO: improve resource locating for API
ROOT_PATH = Path.home().joinpath(".radical_api/lights")
ROOT_PATH.mkdir(parents=True, exist_ok=True)

# make this rescan if light is not found on network
@router.get("/scan")
async def get_lights(force: bool = False, access_token: APIKey = Depends(get_api_key)) -> list[pywizlight.wizlight]:
    if not ROOT_PATH.joinpath("lights.json").exists() or force:
        bulbs = await pywizlight.discovery.discover_lights()
        with ROOT_PATH.joinpath("lights.json").open("w+") as f:
            for bulb in bulbs:
                f.write(f"{bulb.ip}\n")
    else:
        bulbs = []
        for line in ROOT_PATH.joinpath("lights.json").read_text().split():
            bulbs.append(pywizlight.wizlight(line))
    return bulbs

@router.get("/on")
async def lights_on(scene: str = None, access_token: APIKey = Depends(get_api_key)) -> None:
    for light in await get_lights(access_token):
        if scene is not None:
            await light.turn_on(pywizlight.PilotBuilder(scene = get_id_from_scene_name(scene)))
        else:
            await light.turn_on()

@router.get("/off")
async def lights_off(access_token: APIKey = Depends(get_api_key)) -> None:
    for light in await get_lights(access_token):
        await light.turn_off()