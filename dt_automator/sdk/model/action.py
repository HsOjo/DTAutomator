import random

from pyandroidtouch import PyAndroidTouch

import dt_automator.sdk.model as M
from dt_automator.maker.model import MakerActionModel


class ActionModel(MakerActionModel):
    @staticmethod
    def random_position(object_: 'M.ObjectModel', px, py):
        x, y, w, h = object_.rect
        w2, h2 = int(w / 2), int(h / 2)
        ox, oy = x + w2, y + h2
        ax, ay = abs(px), abs(py)
        rad_h = abs(w2 - ax)
        rad_v = abs(h2 - ay)
        px += ox + random.randint(-rad_h, rad_h)
        py += oy + random.randint(-rad_v, rad_v)
        return px, py

    def do(self, pat: PyAndroidTouch, object_: 'M.ObjectModel'):
        if self.type == self.TYPE_TAP:
            px, py = self.random_position(object_, self.params.get('x'), self.params.get('y'))
            pat.tap(
                x=px, y=py, press_time=self.params.get('press_time', 100), count=self.params.get('count', 1),
                finger=self.params.get('finger', 1), finger_distance=self.params.get('finger_distance', 64),
                finger_degree=self.params.get('finger_degree', 0),
            )
        elif self.type == self.TYPE_SWIPE:
            sx, sy = self.random_position(object_, self.params.get('start_x'), self.params.get('start_y'))
            ex, ey = self.random_position(object_, self.params.get('end_x'), self.params.get('end_y'))
            pat.swipe(
                start_x=sx, start_y=sy, end_x=ex, end_y=ey,
                press_time=self.params.get('press_time'), time=self.params.get('time'),
                finger=self.params.get('finger'), finger_distance=self.params.get('finger_distance'),
            )
