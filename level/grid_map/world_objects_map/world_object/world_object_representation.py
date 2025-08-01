from pytiling import GridElement
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytiling import GridLayer


class WorldObjectRepresentation(GridElement):
    """A representation of a world object (parent of game entities). Its name should be the same as the canvas object that represents it"""

    def __init__(
        self, position: tuple[int, int], name: str, tags: list[str] = [], **args
    ):
        super().__init__(position, name, **args)
        self.tags = tags

    @property
    def layer(self):
        return super().layer

    @layer.setter
    def layer(self, layer: "GridLayer"):
        self._layer = layer

    def add_tag(self, tag: str):
        self.tags.append(tag)

    @property
    def canvas_object_name(self):
        variation_tag = next(
            (tag for tag in self.tags if tag.startswith("variation_")), None
        )
        if not variation_tag:
            return self.name
        return variation_tag.replace("variation_", "")
