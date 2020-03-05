from typing import List

from dt_automator.base.model import BaseModel


class FeatureModel(BaseModel):
    DETECT_WEIGHT_MIN = 1
    DETECT_WEIGHT_MAX = 10

    def __init__(self):
        self.name = ''
        self.rect = []  # type: List[int]
        self.detect_weight = self.DETECT_WEIGHT_MIN
