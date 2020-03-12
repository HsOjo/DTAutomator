from io import BytesIO

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

    @property
    def actions_name(self):
        return [action.name for action in self.actions]

    def action(self, name):
        for action in self.actions:
            if name == action.name:
                return action

    def image(self, img_data: bytes):
        img = self.img
        if img_data is not None:
            img = ImageModel()
            with BytesIO(img_data) as io_img:
                image = img_open(io_img)
                img.load_image(image, *self.rect)

        w, h = img.w, img.h
        if w == 0 or h == 0:
            return None

        return img

    def text_image(self, img_data: bytes, px_distance=0, separate_chars=False):
        if self.type != self.TYPE_TEXT:
            return None
        img = self.image(img_data)
        color = self.params.get('color')
        img_data = img.dump_text_image(color, px_distance=px_distance, separate_chars=separate_chars)

        return img_data
