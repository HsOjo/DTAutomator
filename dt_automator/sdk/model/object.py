from dt_automator.maker.model import ObjectModel as MakerObjectModel
from .image import ImageModel


class ObjectModel(MakerObjectModel):
    _sub_model = dict(
        **MakerObjectModel._sub_model,
        img=ImageModel,
    )

    def __init__(self):
        super().__init__()
        self.img = ImageModel()
