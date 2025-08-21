from .level_toggler import LevelToggler
import json
from pytiling.serialization import map_from_dict
from pathlib import Path
from .config import LEVEL_SAVE_FOLDER_PATH
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from .grid_map import MixedMap


class Level:

    def __init__(
        self,
        mixed_map: "MixedMap",
    ):
        self.map = mixed_map

        self.toggler = LevelToggler()

        self._name = "My custom level"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def to_dict(self):
        return {
            "_name": self._name,
            "map": self.map.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        map_obj = cast("MixedMap", map_from_dict(data["map"]))
        instance = cls(mixed_map=map_obj)
        instance.name = data["_name"]
        return instance

    @staticmethod
    def load(filepath: str):
        with open(filepath, "r") as file:
            data = json.load(file)
        level = Level.from_dict(data)
        return level

    @property
    def save_file_path(self):
        """
        Dynamically generates the save file path.
        """
        return Path(LEVEL_SAVE_FOLDER_PATH) / Path(self.name) / f"level.json"

    @property
    def same_name_saved(self):
        return self.save_file_path.parent.is_dir() if self.save_file_path else None

    def save(self):
        if not self.save_file_path:
            raise ValueError("Save file path is not set for the level.")

        self.save_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.save_file_path, "w") as file:
            json.dump(self.to_dict(), file, indent=2)

    @property
    def issues(self):
        issues: list[str] = []

        essentials_layer = self.map.get_layer("essentials")
        delver = essentials_layer.has_element_named("delver")
        if not delver:
            issues.append("The delver needs to be placed on the level.")

        goal = essentials_layer.has_element_named("goal")
        if not goal:
            issues.append("The goal needs to be placed on the level.")

        return issues
