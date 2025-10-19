from pytiling import GridMap
from typing import TYPE_CHECKING, cast
from .editor_tilemap import EditorTilemap
from .world_objects_map import WorldObjectsMap
from level.config import LAYER_ORDER

if TYPE_CHECKING:
    from level.grid_map.editor_tilemap.editor_tilemap_layer import (
        EditorTilemapLayer,
    )
    from level.grid_map.world_objects_map.world_objects_layer.world_objects_layer import (
        WorldObjectsLayer,
    )
    from pytiling import AutotileTile


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
            tile_size, grid_size, min_grid_size, max_grid_size, mixed_map=self
        )
        self.world_objects_map = WorldObjectsMap(
            tile_size, grid_size, min_grid_size, max_grid_size, mixed_map=self
        )

    def to_dict(self):
        """Serialize the map to a dictionary."""
        return {
            "__class__": "MixedMap",
            "tile_size": self.tile_size,
            "grid_size": self.grid_size,
            "min_grid_size": self.min_grid_size,
            "max_grid_size": self.max_grid_size,
            "tilemap": self.tilemap.to_dict(),
            "world_objects_map": self.world_objects_map.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize a map from a dictionary."""
        instance = cls._instance_from_data(data)

        instance.tilemap = EditorTilemap.from_dict(data["tilemap"])
        instance.tilemap.mixed_map = instance
        instance.world_objects_map = WorldObjectsMap.from_dict(
            data["world_objects_map"]
        )
        instance.world_objects_map.mixed_map = instance

        instance.populate_layers()

        # After all layers are loaded into the sub-maps and populated into the
        # main map, establish the concurrences.
        all_layers_data = (
            data["tilemap"]["layers"] + data["world_objects_map"]["layers"]
        )

        cls._setup_concurrency_from_data(all_layers_data, instance)

        return instance

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

    def expand_towards(self, direction, size=1):
        new_positions = super().expand_towards(direction, size)

        fill_tiles: list["AutotileTile"] = []
        if not new_positions:
            return new_positions

        for x, y in new_positions:
            tile = self.tilemap.create_basic_platform_at((x, y), apply_formatting=False)
            if tile:
                fill_tiles.append(tile)

        for tile in fill_tiles:
            tile.format()

        return new_positions

    def reduce_towards(self, direction, size=1):
        return super().reduce_towards(direction, size)
