from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import dill
from pathlib import Path
import json

if TYPE_CHECKING:
    from .grid_map import MixedMap

current_dir = Path(__file__).parent.absolute()
config_path = current_dir / "config.json"
with open(config_path, "r") as file:
    config_data = json.load(file)

SAVE_FOLDER_PATH = Path(config_data["save_folder_path"])

class Level:

    def __init__(
        self,
        map: "MixedMap",
    ):
        self.map = map

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

        self._name = "My custom level"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __getstate__(self):
        state = self.__dict__.copy()
        state["selector"] = None
        state["toggler"] = None

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    @property
    def same_name_saved(self):
        return self.save_file_path.is_file() if self.save_file_path else None

    def save(self):
        if not self.save_file_path:
            raise ValueError("Save file path is not set for the level.")

        with open(self.save_file_path, "wb") as file:
            dill.dump(self, file)

    @property
    def save_file_path(self):
        return SAVE_FOLDER_PATH / f"{self.name}.dill" if SAVE_FOLDER_PATH else None

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
