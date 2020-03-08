from typing import List

from dt_automator.base.model import BaseModel


class FeatureModel(BaseModel):
    DETECT_WEIGHT_MIN = 1
    DETECT_WEIGHT_MAX = 10

    MODE_DIFFERENCE = 0
    MODE_DISTANCE = 1

    ALL_MODES = {
        'Difference': MODE_DIFFERENCE,
        'Distance': MODE_DISTANCE,
    }
    ALL_MODES_REV = dict((v, k) for k, v in ALL_MODES.items())

    def __init__(self):
        self.name = ''
        self.rect = []  # type: List[int]
        self.detect_weight = self.DETECT_WEIGHT_MIN
        self.mode = self.MODE_DISTANCE
