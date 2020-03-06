from typing import List, Dict, Any

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
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]

    @property
    def next_scenes(self):
        scenes = {}  # type: Dict[SceneModel, Dict[str, Any]]
        for object_ in self.objects:
            for action in object_.actions:
                scenes[action.dest_scene] = {
                    'object': object_,
                    'action': action,
                }
        return scenes

    def find_paths(self, to, _path:list=None):
        scenes = self._event['get_scenes']()  # type: Dict[SceneModel]
        if _path is None:
            path = []
        else:
            path = _path.copy()
        from_scene = self
        if isinstance(to, str):
            to_scene = scenes[to]
        elif isinstance(to, SceneModel):
            to_scene = to
        else:
            raise Exception('Unsupport "to" type: %s' % to)

        for scene in from_scene.next_scenes:
            p_scene = scene.find_paths(to_scene, path)

        # Todo.