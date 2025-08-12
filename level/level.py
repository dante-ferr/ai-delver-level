from typing import TYPE_CHECKING
from .level_selector import LevelSelector
from .level_toggler import LevelToggler
import dill
from pathlib import Path
from .config import LEVEL_SAVE_FOLDER_PATH


if TYPE_CHECKING:
    from .grid_map import MixedMap


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
        """
        Custom serialization method to explicitly define the object's state.
        This prevents pickling transient or environment-specific attributes
        like Path objects, selectors, or togglers.
        We only serialize the data that is essential to the level's definition.
        """
        return {
            "map": self.map,
            "_name": self._name,
        }

    def __setstate__(self, state):
        """
        Custom deserialization method to reconstruct the object from its state
        and then re-initialize the transient attributes that were not serialized.
        """
        self.__dict__.update(state)

        # Re-create the objects that were not part of the serialized state
        self.selector = LevelSelector()
        self.toggler = LevelToggler()

    @property
    def save_file_path(self):
        """
        Dynamically generates the save file path.
        This property is not serialized, thus avoiding the ModuleNotFoundError.
        """
        return Path(LEVEL_SAVE_FOLDER_PATH) / Path(self.name) / f"level.dill"

    @property
    def same_name_saved(self):
        return self.save_file_path.parent.is_dir() if self.save_file_path else None

    def save(self):
        if not self.save_file_path:
            raise ValueError("Save file path is not set for the level.")

        self.save_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.save_file_path, "wb") as file:
            dill.dump(self, file)

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
