from typing import List

from dt_automator.base.model import BaseModel
from .feature import FeatureModel
from .object import ObjectModel


class SceneModel(BaseModel):
    _sub_model = dict(
        features=(list, FeatureModel),
        objects=(list, ObjectModel),
    )

    def __init__(self):
        self.name = ''
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]
