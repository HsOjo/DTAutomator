from typing import List, Dict, Any

from PIL.Image import Image

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
    def next_scenes_info(self):
        scenes = []  # type: List[Dict[str, Any]]
        for object_ in self.objects:
            for action in object_.actions:
                scenes.append(dict(
                    scene=action.dest_scene,
                    object=object_,
                    action=action,
                ))
        return scenes

    def find_paths(self, to, _path: list = None, _distance=1):
        scenes = self._event['get_scenes']()  # type: Dict[str, SceneModel]
        _paths = []
        if _path is None:
            _path = [dict(scene=self.name, object=None, action=None, distance=0)]
        path = _path.copy()
        if isinstance(to, str):
            to_scene = scenes[to]
        elif isinstance(to, SceneModel):
            to_scene = to
        else:
            raise Exception('Unsupport "to" type: %s' % to)

        path_scene_names = [i['scene'] for i in path]
        for info in self.next_scenes_info:
            path = _path.copy()
            info['distance'] = _distance
            scene = scenes.get(info['scene'])  # type: SceneModel
            if scene is not None and scene.name not in path_scene_names:
                path.append(info)
                if scene == to_scene:
                    _paths.append(path)
                else:
                    _paths += scene.find_paths(to_scene, path, _distance + 1)

        return _paths

    def compare(self, img: Image):
        ma = img.width * img.height
        if len(self.features) == 0 or ma == 0:
            return 0

        mv = 0
        v = 0
        for feature in self.features:
            _, _, w, h = feature.rect
            dv, dvm = feature.img.compare(img, feature.mode, *feature.rect, feature.detect_weight)
            v += dv
            mv += dvm

        return 1 - (v / mv)
