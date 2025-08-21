from pytiling import Tileset
from ..grid_map.editor_tilemap.editor_tilemap_layer import EditorTilemapLayer
from ..grid_map.world_objects_map import WorldObjectsLayer
from ..grid_map import MixedMap
from ..level import Level
from level.config import *

MAP_SIZE = (START_MAP_WIDTH, START_MAP_HEIGHT)
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)


class LevelFactory:

    def create_level(self):

        mixed_map = MixedMap(TILE_SIZE, MAP_SIZE, MIN_GRID_SIZE, MAX_GRID_SIZE)
        self.tilemap = mixed_map.tilemap
        self.world_objects_map = mixed_map.world_objects_map
        self._configure_tilemap()
        self._configure_world_objects_map()
        mixed_map.populate_layers()

        level = Level(mixed_map)
        level.map.add_layer_concurrence("walls", "essentials")

        self._create_starting_tiles()
        self.tilemap.lock_boundary_walls_if_needed()
        self._create_starting_world_objects()

        return level

    def _configure_tilemap(self):
        layers = {
            "floor": EditorTilemapLayer(
                "floor",
                Tileset(str(ASSETS_PATH / "img/tilesets/dungeon/floor.png")),
                str(ASSETS_PATH / "svg/floor.svg"),
            ),
            "walls": EditorTilemapLayer(
                "walls",
                Tileset(str(ASSETS_PATH / "img/tilesets/dungeon/walls.png")),
                str(ASSETS_PATH / "svg/walls.svg"),
            ),
        }

        for layer_name in LAYER_ORDER:
            if layer_name in TILEMAP_LAYER_NAMES:
                self.tilemap.add_layer(layers[layer_name])

        self.tilemap.add_layer_concurrence("walls", "floor")

    def _create_starting_tiles(self):
        for x in range(1, self.tilemap.grid_size[0] - 1):
            for y in range(1, self.tilemap.grid_size[1] - 1):
                self.tilemap.create_basic_floor_at((x, y), apply_formatting=False)

        for position in self.tilemap.get_edge_positions():
            self.tilemap.create_basic_wall_at(position, apply_formatting=False)

        self.tilemap.format_all_tiles()

    def _configure_world_objects_map(self):
        essentials = WorldObjectsLayer(
            "essentials", str(ASSETS_PATH / "svg/important.svg")
        )
        self.world_objects_map.add_layer(essentials)

    def _create_starting_world_objects(self):
        essentials_layer = self.world_objects_map.get_layer("essentials")

        essentials_layer.create_world_object_at(
            START_DELVER_POSITION,
            "delver",
        )
        # essentials_layer.canvas_object_manager.get_canvas_object(
        #     "battery_snack"
        # ).create_element_callback(START_GOAL_POSITION)
