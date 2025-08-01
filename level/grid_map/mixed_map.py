from pytiling import GridMap
import json
from typing import TYPE_CHECKING, cast
from .editor_tilemap import EditorTilemap
from .world_objects_map import WorldObjectsMap
import os
import json

if TYPE_CHECKING:
    from level.canvas_object import CanvasObject
    from level.grid_map.editor_tilemap.editor_tilemap_layer import (
        EditorTilemapLayer,
    )
    from level.grid_map.world_objects_map.world_objects_layer.world_objects_layer import (
        WorldObjectsLayer,
    )


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "..", "config.json")
with open(config_path, "r") as file:
    config_data = json.load(file)

LAYER_ORDER = config_data["layer_order"]


class MixedMap(GridMap):
    def __init__(
        self,
        tile_size: tuple[int, int],
        grid_size: tuple[int, int],
        min_grid_size: tuple[int, int],
        max_grid_size: tuple[int, int],
    ):
        super().__init__(tile_size, grid_size, min_grid_size, max_grid_size)

        self.tilemap = EditorTilemap(
            self, tile_size, grid_size, min_grid_size, max_grid_size
        )
        self.world_objects_map = WorldObjectsMap(
            self, tile_size, grid_size, min_grid_size, max_grid_size
        )

    def populate_layers(self):
        for layer_name in LAYER_ORDER:
            if self.tilemap.has_layer(layer_name):
                self.add_layer(self.tilemap.get_layer(layer_name))

            if self.world_objects_map.has_layer(layer_name):
                self.add_layer(self.world_objects_map.get_layer(layer_name))

    def get_tilemap_layer(self, name: str):
        """Get a tilemap layer. Use this function if you want the tilemap layer type assigned to a variable."""
        return self.tilemap.get_layer(name)

    def get_world_objects_layer(self, name: str):
        """Get a world objects layer. Use this function if you want the world objects layer type assigned to a variable."""
        return self.world_objects_map.get_layer(name)

    def get_layer(self, name: str):
        """Get a layer by its name."""
        return cast("WorldObjectsLayer | EditorTilemapLayer", super().get_layer(name))

    @property
    def layers(self):
        """Returns a list of layers in the correct order."""
        return cast(list["WorldObjectsLayer | EditorTilemapLayer"], super().layers)

    @property
    def grid_size(self):
        return self.tilemap.grid_size

    @grid_size.setter
    def grid_size(self, value: tuple[int, int]):
        self.tilemap.grid_size = value
        self.world_objects_map.grid_size = value
        self._grid_size = self.clamp_size(value)

    @property
    def canvas_objects(self):
        canvas_objects: dict[str, "CanvasObject"] = {}

        for layer in self.layers:
            layer = cast("WorldObjectsLayer", layer)
            for canvas_object in layer.canvas_object_manager.canvas_objects.values():
                canvas_objects[canvas_object.name] = canvas_object

        return canvas_objects

    def get_canvas_object(self, canvas_object_name: str) -> "CanvasObject":
        return self.canvas_objects[canvas_object_name]
