from typing import Callable
from PIL import Image


class CanvasObject:
    def __init__(
        self,
        name: str,
        image_path: str,
        create_element_callback: Callable,
        remove_element_callback: Callable | None = None,
        unique: bool = False,
    ):
        self.name = name
        self.create_element_callback = create_element_callback
        self.remove_element_callback = remove_element_callback
        self.unique = unique

        self.image = Image.open(image_path)
