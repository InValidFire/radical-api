import logging

import pywizlight
from pywizlight.scenes import get_id_from_scene_name, SCENES

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from core.storage import Storage

from .security import get_api_key

logger = logging.getLogger("lights")
router = APIRouter(prefix="/lights", tags=["lights"])

storage = Storage("lights")

async def get_lights(access_token: APIKey = Depends(get_api_key), target: str = None) -> list[pywizlight.wizlight]:
    try:
        bulb_ips = storage.read_file("lights.json")
        bulbs = []
        for ip in bulb_ips:
            if target is not None and ip != target:
                continue
            bulbs.append(pywizlight.wizlight(ip))
        if len(bulbs) == 0:
            raise ValueError
    except (FileNotFoundError, ValueError):
        storage.write_file("lights.json", await scan_lights(access_token))        
    return bulbs

@router.get("/scan")
async def scan_lights(access_token: APIKey = Depends(get_api_key)) -> list[str]:
    bulbs = await pywizlight.discovery.discover_lights()
    bulb_ips = []
    for bulb in bulbs:
        bulb_ips.append(bulb.ip)
    return bulb_ips

# make this rescan if light is not found on network

@router.get("/on")
async def lights_on(scene: str = None, target: str = None, access_token: APIKey = Depends(get_api_key)) -> None:
    for light in await get_lights(access_token, target):
        if scene is not None:
            await light.turn_on(pywizlight.PilotBuilder(scene = get_id_from_scene_name(scene)))
        else:
            await light.turn_on()

@router.get("/off")
async def lights_off(target: str, access_token: APIKey = Depends(get_api_key)) -> None:
    for light in await get_lights(access_token, target):
        await light.turn_off()

@router.get("/scenes")
async def lights_scenes(access_token: APIKey = Depends(get_api_key)) -> None:
    return SCENES
