import sys

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

import subprocess
from .security import get_system_key

router = APIRouter()


@router.post("/system/update")
def update(access_token: APIKey = Depends(get_system_key)):
    output = subprocess.check_output(['git', 'pull'], encoding='utf-8')
    sys.exit()
