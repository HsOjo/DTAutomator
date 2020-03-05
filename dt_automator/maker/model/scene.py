from typing import List

from dt_automator.base.model import BaseModel
from .feature import FeatureModel
from .object import ObjectModel


class SceneModel(BaseModel):
    _sub_model = dict(
        features=(list, FeatureModel),
        objects=(list, ObjectModel),
    )
    _ignore_attrs = ['img_path']

    def __init__(self, event: dict):
        self._event = event
        self.name = ''
        self.img = ''
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]

    @property
    def img_path(self):
        return self._event['get_path'](self.img)

    def rename(self, new):
        img_name = self.img
        self.name = new
        self.img = '%s.png' % new
        self._event['move_file'](img_name, self.img)
