from typing import List

from dt_automator.base.model import BaseModel


class ImageModel(BaseModel):
    def __init__(self):
        self.w = 0
        self.h = 0
        self.pxs = []  # type: List[int]

    def load_image(self, img_data: bytes):
        pass

    def pixel(self, x, y):
        index = (y * self.w + x) * 4
        [r, g, b, a] = self.pxs[index:index + 4]
        return r, g, b, a
