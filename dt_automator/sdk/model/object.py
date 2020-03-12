from io import BytesIO

import pytesseract
from PIL.Image import open as img_open

from dt_automator.maker.model import MakerObjectModel
from .action import ActionModel
from .image import ImageModel


class ObjectModel(MakerObjectModel):
    _ignore_repr_attrs = ['img']

    _sub_model = dict(
        actions=(list, ActionModel),
        img=ImageModel,
    )

    def __init__(self):
        super().__init__()
        self.img = ImageModel()

    def detect_text(self, img_data: bytes, px_distance=0, lang='eng'):
        img = self.img
        if img_data is not None:
            img = ImageModel()
            with BytesIO(img_data) as io_img:
                image = img_open(io_img)
                img.load_image(image, *self.rect)

        w, h = img.w, img.h
        if self.type != self.TYPE_TEXT or w == 0 or h == 0:
            return None

        color = self.params.get('color')
        img_data = img.dump_text_image(color, px_distance=px_distance)

        with BytesIO(img_data) as io_img:
            image = img_open(io_img)
            result = pytesseract.image_to_string(image, lang)

        return result
