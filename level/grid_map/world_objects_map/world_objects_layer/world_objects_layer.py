from pytiling import GridLayer
from level.canvas_object import CanvasObjectsManager
from ..world_object import WorldObjectRepresentation


class WorldObjectsLayer(GridLayer):
    def __init__(self, name: str, icon_path: str):
        super().__init__(name)
        self.icon_path = icon_path
        self.canvas_object_manager = CanvasObjectsManager()

    def create_world_object_at(self, position: tuple[int, int], name: str, **args):
        world_object = WorldObjectRepresentation(position, name, **args)
        self.add_element(world_object)
        return world_object
