from dt_automator.maker.model import MakerObjectModel
from .image import ImageModel
from .action import ActionModel


class ObjectModel(MakerObjectModel):
    _ignore_repr_attrs = ['img']

    _sub_model = dict(
        actions=(list, ActionModel),
        img=ImageModel,
    )

    def __init__(self):
        super().__init__()
        self.img = ImageModel()
