from pytiling import TilemapLayer
from level.canvas_object import CanvasObjectsManager


class EditorTilemapLayer(TilemapLayer):
    def __init__(self, name: str, tileset, icon_path: str):
        super().__init__(name, tileset)
        self.icon_path = icon_path
        self.canvas_object_manager = CanvasObjectsManager()
