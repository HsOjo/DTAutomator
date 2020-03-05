from dt_automator.maker.model import ObjectModel as MakerObjectModel
from .image import ImageModel


class ObjectModel(MakerObjectModel):
    def __init__(self):
        super().__init__()
        self.img = ImageModel()
