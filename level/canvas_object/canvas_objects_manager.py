from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from level.canvas_object import CanvasObject


class CanvasObjectsManager:
    def __init__(self):
        self.canvas_objects: dict[str, "CanvasObject"] = {}

    def add_canvas_object(self, canvas_object: "CanvasObject"):
        self.canvas_objects[canvas_object.name] = canvas_object

    def get_canvas_object(self, canvas_object_name: str) -> "CanvasObject":
        return self.canvas_objects[canvas_object_name]
