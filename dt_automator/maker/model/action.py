from dt_automator.base.model import BaseModel


class ActionModel(BaseModel):
    TYPE_TAP = 0
    TYPE_SWIPE = 1
    TYPE_PRESS = 2

    ALL_TYPES = {
        'Tap': TYPE_TAP,
        'Swipe': TYPE_SWIPE,
        'Press': TYPE_PRESS,
    }
    ALL_TYPES_REV = dict((v, k) for k, v in ALL_TYPES.items())

    SCENE_NONE = 'None'

    def __init__(self, parent=None):
        self.name = ''
        self.type = self.TYPE_TAP
        self.dest_scene = self.SCENE_NONE
        self.params = {}
        self._parent = parent
