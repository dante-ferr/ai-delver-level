from ._level_factory import LevelFactory
from ._level_factory import LevelFactory
from pathlib import Path
from typing import cast, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from ..level import Level


class LevelLoader:

    def __init__(self):
        self.factory = LevelFactory()
        self._create_new_level()

    def load_level(self, dir_path: str | Path, file_name: str = "level.json"):
        """Loads a level from a file. The path of the level directory must be provided (instead of the level file itself)."""
        if type(dir_path) == str:
            dir_path = Path(dir_path)
        dir_path = cast(Path, dir_path)
        file_path = dir_path / file_name

        if file_path.is_file():
            from ..level import Level

            return Level.load(str(file_path))
        else:
            logging.info("Creating new level")
            self._create_new_level()

    @property
    def level(self):
        if self._level is None:
            raise ValueError("The level doesn't exist.")
        return self._level

    @level.setter
    def level(self, value: "Level"):
        """Sets the level to the given level."""
        self._level = value

    def _create_new_level(self):
        self._level: "Level" = self.factory.create_level()
