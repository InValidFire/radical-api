import logging
from typing import Optional
import giteapy
import json

from pathlib import Path
from fastapi import APIRouter, Header, Query, HTTPException
from gitea.gitea import Repository

ROOT_PATH = Path.home().joinpath(".radical_api/gitea")

logger = logging.getLogger("gitea")
router = APIRouter()

@router.get("/gitea/latest")
def get_latest_version(base_url: Optional[str] = Header(None), author: str = Query(None), repo: str = Query(None), pre_releases: bool = Query(False)):
    with ROOT_PATH.joinpath("keys.json").open("r") as fp:
        data: dict = json.load(fp)
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