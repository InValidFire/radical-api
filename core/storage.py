import json

from pathlib import Path

class Storage:
    """Handles all filesystem interactions for the API"""
    def __init__(self, router: str) -> None:
        self.root = Path.home().joinpath(".radical_api").joinpath(router)
        self.root.mkdir(exist_ok=True, parents=True)

    def _get_file(self, path: str) -> Path:
        return self.root.joinpath(path)

    def write_file(self, name: str, data: dict):
        file = self._get_file(name)
        file.touch(exist_ok=True)
        with file.open("w+") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def read_file(self, name: str) -> dict:
        file = self._get_file(name)
        if not file.exists():
            return {}
        with file.open("r+") as f:
            data = json.load(f)
        return data

    def delete_file(self, name: str):
        file = self._get_file(name)
        file.unlink(missing_ok=True)

    def rename_file(self, old_name: str, new_name: str):
        file = self._get_file(old_name)
        new_file = self.root.joinpath(new_name)
        file.rename(new_file)