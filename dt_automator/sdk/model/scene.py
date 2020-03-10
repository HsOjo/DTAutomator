from typing import List, Dict, Any

from PIL.Image import Image

from dt_automator.maker.model import MakerSceneModel
from .feature import FeatureModel
from .object import ObjectModel
from .path import PathModel, PathNodeModel


class SceneModel(MakerSceneModel):
    _sub_model = dict(
        features=(list, FeatureModel),
        objects=(list, ObjectModel),
    )

    def __init__(self, event: dict):
        self._event = event
        self._accuracy = 0
        self.name = ''
        self.features = []  # type: List[FeatureModel]
        self.objects = []  # type: List[ObjectModel]

    @property
    def next_scenes_info(self):
        scenes = []  # type: List[Dict[str, Any]]
        for object_ in self.objects:
            for action in object_.actions:
                scenes.append(dict(
                    src_scene=self.name,
                    dest_scene=action.dest_scene,
                    object=object_,
                    action=action,
                ))
        return scenes

    @property
    def accuracy(self):
        return self._accuracy

    def _find_paths(self, to, _nodes: list = None, _from=None):
        if _from is None:
            _from = self
        if _nodes is None:
            _nodes = []

        scenes = self._event['get_scenes']()  # type: Dict[str, SceneModel]
        if isinstance(to, str):
            to_scene = scenes[to]
        elif isinstance(to, SceneModel):
            to_scene = to
        else:
            raise Exception('Unsupport "to" type: %s' % to)

        paths = []  # type: List[PathModel]

        nodes = _nodes.copy()
        nodes_scene_name = [_from.name] + [node.dest_scene.name for node in nodes]
        for info in self.next_scenes_info:
            nodes = _nodes.copy()
            dest_scene = scenes.get(info['dest_scene'])  # type: SceneModel
            info['dest_scene'] = dest_scene
            info['src_scene'] = self
            if dest_scene is not None and dest_scene.name not in nodes_scene_name:
                node = PathNodeModel()
                node.load_data(**info)
                nodes.append(node)

                if dest_scene == to_scene:
                    path = PathModel()
                    path.load_data(nodes=nodes)
                    paths.append(path)
                else:
                    paths += dest_scene._find_paths(to_scene, nodes, _from)

        return paths

    def find_paths(self, to):
        paths = sorted(self._find_paths(to), key=lambda x: x.distance)
        return paths

    def compare(self, img: Image):
        ma = img.width * img.height
        if len(self.features) == 0 or ma == 0:
            return False

        mv = 0
        v = 0
        for feature in self.features:
            _, _, w, h = feature.rect
            dv, dvm = feature.img.compare(img, feature.mode, *feature.rect, feature.detect_weight)
            v += dv
            mv += dvm

        self._accuracy = 1 - (v / mv)
        return True
