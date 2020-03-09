from typing import List

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
