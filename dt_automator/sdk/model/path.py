import time
from typing import List

from pyandroidtouch import PyAndroidTouch

import dt_automator.sdk.model as M
from ...base.model import BaseModel


class PathNodeModel(BaseModel):
    def __init__(self):
        self.src_scene: 'M.SceneModel' = None
        self.dest_scene: 'M.SceneModel' = None
        self.object: 'M.ObjectModel' = None
        self.action: 'M.ActionModel' = None

    def __repr__(self):
        return '<%s %s %s>' % (self.__class__.__name__, self.src_scene, self.dest_scene)


class PathModel(BaseModel):
    _sub_model = dict(
        nodes=(list, PathNodeModel),
    )

    def __init__(self):
        self.nodes = []  # type: List[PathNodeModel]

    def __iter__(self):
        return self.nodes.__iter__()

    def __getitem__(self, item):
        return self.nodes.__getitem__(item)

    @property
    def distance(self):
        return sum([node.action.distance for node in self.nodes])

    def do_actions(self, pat: PyAndroidTouch, hook_did_action=None):
        def do_action(action: M.ActionModel):
            action.do(pat, node.object)
            time.sleep(node.action.wait / 1000)
            if hook_did_action is not None:
                if not hook_did_action(node):
                    return False

        for node in self.nodes:
            actions_map = dict((action.name, action) for action in node.object.actions)
            if node.action.type == M.ActionModel.TYPE_GROUP:
                actions_key = node.action.params.get('actions', '').split(',')
                for k in actions_key:
                    action = actions_map[k]  # type: M.ActionModel
                    do_action(action)
            else:
                do_action(node.action)

        return True
