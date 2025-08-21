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

    def load_level(self, path: str | Path):
        """Loads a level from a file. The path of the level directory must be provided (instead of the level file itself)."""
        if type(path) == str:
            path = Path(path)
        path = cast(Path, path)
        file_path = path / "level.json"

        if file_path.is_file():
            from ..level import Level

            self._level = Level.load(str(file_path))
        else:
            logging.info("Creating new level")
            self._create_new_level()

        return self.level

    @property
    def level(self):
        if self._level is None:
            raise ValueError("The level doesn't exist.")
        return self._level

    @level.setter
    def level(self, value: "Level"):
        """Sets the level to the given level. This should only be used for testing."""
        return self._level

    def _create_new_level(self):
        self._level: "Level" = self.factory.create_level()
