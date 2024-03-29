import logging
from typing import Optional
import giteapy

from fastapi import APIRouter, Header, Query, HTTPException

from core.storage import Storage

storage = Storage("gitea")

logger = logging.getLogger("gitea")
router = APIRouter()

@router.get("/gitea/latest")
def get_latest_version(base_url: Optional[str] = Header(None), author: str = Query(None), repo: str = Query(None), pre_releases: bool = Query(False)):
    data = storage.read_file("keys.json")
    if base_url in data.keys():
        config = giteapy.Configuration()
        config.api_key['access_token'] = data[base_url]
        config.host = base_url + "/api/v1"
        api = giteapy.RepositoryApi(giteapy.ApiClient(config))
        response = api.repo_list_releases(author, repo)
        if len(response) == 0:
            raise HTTPException(404, "No releases for given repository.")

        for release in response:
            release: giteapy.Release
            if pre_releases:
                return release.name
            elif not pre_releases and release.prerelease:
                continue
            elif not pre_releases and not release.prerelease:
                return release.name
    else:
        raise HTTPException(400, "API cannot access this Gitea instance.")