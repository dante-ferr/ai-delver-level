from pytiling import Tilemap
from typing import TYPE_CHECKING, cast, Literal
import os


if TYPE_CHECKING:
    from .editor_tilemap_layer import EditorTilemapLayer
    from pytiling import Tile, GridElement, GridLayer, AutotileTile
    from ..mixed_map import MixedMap


class EditorTilemap(Tilemap):
    SHALLOW_PLATFORMS_VARIATIONS = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "shallow_platforms_variations.json"
    )

    def __init__(
        self,
        tile_size: tuple[int, int],
        grid_size: tuple[int, int] = (5, 5),
        min_grid_size: tuple[int, int] = (5, 5),
        max_grid_size: tuple[int, int] = (100, 100),
        mixed_map: "MixedMap | None" = None,
    ):
        """
        Initialize the EditorTilemap with optional mixed_map reference.
        If mixed_map is not provided right away, it can must be set later to allow
        acessing the MixedMap methods like 'reduce_towards' and 'expand_towards'.
        """
        super().__init__(tile_size, grid_size, min_grid_size, max_grid_size)
        self._mixed_map = mixed_map

    def to_dict(self):
        """Serialize the tilemap to a dictionary."""
        data = super().to_dict()
        data["__class__"] = "EditorTilemap"
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Deserialize a tilemap from a dictionary.
        Note: This does not handle layer concurrences. The parent MixedMap is responsible for that.
        """
        return cls._from_dict_base(data)

    def add_layer(self, layer: "GridLayer", position: int | Literal["end"] = "end"):
        """Add a layer to the tilemap."""
        super().add_layer(layer, position)

    def get_layer(self, name: str) -> "EditorTilemapLayer":
        """Get a layer by its name."""
        return cast("EditorTilemapLayer", super().get_layer(name))

    def create_basic_platform_at(self, position: tuple[int, int], **args):
        platforms = self.get_layer("platforms")
        tile = platforms.create_autotile_tile_at(
            position,
            "platform",
            **args,
        )
        if tile is not None:

            def _callback(sender, tile: "AutotileTile"):
                if tile.is_shallow:
                    tile.add_variations_from_json(self.SHALLOW_PLATFORMS_VARIATIONS)

            tile.events["post_autotile"].connect(_callback, weak=False)

            self._reduce_grid_size_if_needed(tile)

        return tile

    def remove_platform_at(self, position: tuple[int, int], apply_formatting=False):
        platforms = self.get_layer("platforms")
        removed_tile = platforms.remove_tile_at(position, apply_formatting)
        if removed_tile is not None:
            self._expand_grid_size_if_needed(removed_tile)

        return removed_tile

    def _reduce_grid_size_if_needed(self, new_tile: "Tile"):
        tile_x, tile_y = new_tile.position
        platforms = self.get_layer("platforms")

        def _process_line(edge, platforms=platforms):
            full_of_platforms = all(
                tile is not None and tile.name == "platform"
                for tile in platforms.get_edge_tiles(edge, retreat=1)
            )

            if not full_of_platforms:
                return
            deleted_elements = self.mixed_map.reduce_towards(edge)
            if not deleted_elements:
                return

            _process_line(edge)

        grid_width, grid_height = self.mixed_map.grid_size

        if tile_x == 1:
            _process_line("left")
        if tile_x == grid_width - 2:
            _process_line("right")
        if tile_y == 1:
            _process_line("top")
        if tile_y == grid_height - 2:
            _process_line("bottom")

    def _expand_grid_size_if_needed(self, new_tile: "Tile"):
        if new_tile.edges is None:
            return
        for edge in new_tile.edges:
            added_positions = self.mixed_map.expand_towards(edge)
            if not added_positions:
                continue

            fill_tiles: list["AutotileTile"] = []
            for x, y in added_positions:
                tile = self.create_basic_platform_at((x, y), apply_formatting=False)
                if tile:
                    fill_tiles.append(tile)

            for tile in fill_tiles:
                tile.format()

        self.lock_boundary_platforms_if_needed()

    def lock_boundary_platforms_if_needed(self):
        platforms = self.get_layer("platforms")
        elements: list["GridElement | None"] = []

        if self.grid_size[0] == self.max_grid_size[0]:
            elements += platforms.get_edge_elements(
                "left"
            ) + platforms.get_edge_elements("right")
        if self.grid_size[1] == self.max_grid_size[1]:
            elements += platforms.get_edge_elements(
                "top"
            ) + platforms.get_edge_elements("bottom")

        for element in elements:
            if element is not None:
                element.locked = True

    @property
    def mixed_map(self):
        if self._mixed_map is None:
            raise ValueError("MixedMap reference is not set.")
        return self._mixed_map

    @mixed_map.setter
    def mixed_map(self, value: "MixedMap | None"):
        """
        Set the mixed_map reference.
        This is useful if the mixed_map is not available during initialization.
        """
        self._mixed_map = value
