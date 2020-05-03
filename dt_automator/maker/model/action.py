from dt_automator.base.model import BaseModel


class ActionModel(BaseModel):
    TYPE_GROUP = -1
    TYPE_TAP = 0
    TYPE_SWIPE = 1

    ALL_TYPES = {
        'Group': TYPE_GROUP,
        'Tap': TYPE_TAP,
        'Swipe': TYPE_SWIPE,
    }
    ALL_TYPES_REV = dict((v, k) for k, v in ALL_TYPES.items())

    PARAM_NONE = 'None'

    PARAMS_COMMON = ['distance', 'wait']

    PARAMS_TYPE = {
        TYPE_GROUP: ['x', 'y', 'actions'],
        TYPE_TAP: ['x', 'y', 'press_time', 'count', 'finger', 'finger_distance', 'finger_degree'],
        TYPE_SWIPE: ['start_x', 'start_y', 'end_x', 'end_y', 'press_time', 'time', 'finger', 'finger_distance'],
    }

    PARAMS_DEFAULT = dict(
        x=0,
        y=0,
        press_time=100,
        count=1,

        start_x=0,
        start_y=0,
        end_x=0,
        end_y=0,
        time=1000,

        distance=1,
        wait=500,

        finger=1,
        finger_distance=64,
        finger_degree=0,

        actions='',
    )

    def __init__(self):
        self.name = ''
        self.type = self.TYPE_TAP
        self.dest_scene = self.PARAM_NONE
        self.params = {}

    @property
    def distance(self):
        return self.params.get('distance', self.PARAMS_DEFAULT['distance'])

    @property
    def wait(self):
        return self.params.get('wait', self.PARAMS_DEFAULT['wait'])
