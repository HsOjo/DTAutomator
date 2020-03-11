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

    def detect_text(self, distance=0, border=2):
        w, h = self.img.w, self.img.h
        if self.type != self.TYPE_TEXT or w == 0 or h == 0:
            return None

        color = self.params.get('color')
        if color is None:
            color = self.img.most_acc_text_color
        rect = self.img.text_rect(color, distance, border)
        img_data = self.img.dump_image(*rect)
        io_img = BytesIO(img_data)
        img = img_open(io_img)
        result = pytesseract.image_to_string(img, 'eng', config='/usr/local/Cellar/tesseract/4.1.1/share/tessdata')
        io_img.close()

        return result
