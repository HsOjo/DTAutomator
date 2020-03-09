from pyandroidtouch import PyAndroidTouch

from dt_automator.maker.model import MakerActionModel


class ActionModel(MakerActionModel):
    def do(self, pat: PyAndroidTouch):
        if self.type == self.TYPE_TAP:
            pat.tap(
                x=self.params['x'], y=self.params['y'],
                press_time=self.params['press_time'], count=self.params['count'],
                finger=self.params['finger'], finger_degree=self.params['finger_degree'],
                finger_distance=self.params['finger_distance'],
            )
        elif self.type == self.TYPE_SWIPE:
            pat.swipe(
                start_x=self.params['start_x'], start_y=self.params['start_y'],
                end_x=self.params['end_x'], end_y=self.params['end_y'],
                press_time=self.params['press_time'], time=self.params['time'],
                finger=self.params['finger'], finger_distance=self.params['finger_distance'],
            )
