from typing import List

from dt_automator.base.model import BaseModel
from .feature import FeatureModel
from .object import ObjectModel


class SceneModel(BaseModel):
    _sub_model = dict(
        features=(list, FeatureModel),
        objects=(list, ObjectModel),
    )

    def __init__(self, event: dict):
        self._event = event
        self.name = ''
        self.img = ''
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]

    @property
    def img_path(self):
        return self._event['get_path'](self.img)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)
