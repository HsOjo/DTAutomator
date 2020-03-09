import json
import zlib
from io import BytesIO
from typing import Dict, List

from PIL.Image import open as img_open, Image
from pyadb import Device

from dt_automator.maker import Project
from dt_automator.maker.model import MakerSceneModel
from dt_automator.sdk.model import SceneModel, ObjectModel, FeatureModel


class DTAutomator:
    def __init__(self, device: Device):
        self._scenes = {}  # type: Dict[str, SceneModel]
        self._event = dict(
            get_scenes=lambda: self._scenes
        )
        self._device = device

    def load_from_maker(self, path_dir: str):
        project = Project.open(path_dir)
        scenes = {}
        for name, scene in project.scenes.items():
            scene: MakerSceneModel
            io_img = open(scene.img_path, 'rb')
            img = img_open(io_img)  # type:Image
            new_scene = SceneModel(self._event)
            new_scene.name = scene.name
            for feature in scene.features:
                new_feature = FeatureModel()
                new_feature.load_data(**feature.data)
                new_feature.img.load_image(img, *feature.rect)
                new_scene.features.append(new_feature)
            for object_ in scene.objects:
                new_object = ObjectModel()
                new_object.load_data(**object_.data)
                new_object.img.load_image(img, *object_.rect)
                new_scene.objects.append(new_object)
            io_img.close()
            scenes[name] = new_scene
        self._scenes = scenes

    def load(self, path: str):
        with open(path, 'rb') as io:
            data = io.read()
        data_str = zlib.decompress(data).decode('utf-8')
        data = json.loads(data_str)
        scenes = {}
        for k, v in data.items():
            scene = SceneModel(self._event)
            scene.load_data(**v)
            scenes[k] = scene
        self._scenes = scenes

    def dump(self, path):
        data = dict((k, v.data) for k, v in self._scenes.items())
        data_str = json.dumps(data, ensure_ascii=False)
        data = zlib.compress(data_str.encode('utf-8'))
        with open(path, 'wb') as io:
            io.write(data)

    def compare_scenes(self, img_data=None):
        if img_data is None:
            img_data = self.screen
        io_img = BytesIO(img_data)
        img = img_open(io_img)
        for scene in self._scenes.values():
            scene.compare(img)
        io_img.close()

    def scene(self, name):
        return self._scenes.get(name)

    def scenes(self, sorted_by_acc=False):
        scenes = list(self._scenes.values())
        if sorted_by_acc:
            scenes = sorted(scenes, key=lambda x: x.accuracy)
        return scenes

    @property
    def most_acc_scene(self):
        scenes = self.scenes(True).copy()
        if len(scenes) > 0:
            return scenes[-1]
        else:
            return None

    @property
    def screen(self):
        return self._device.display.screen_cap()

    def find_paths(self, to, from_=None):
        if isinstance(to, str):
            to = self.scene(to)
        if isinstance(from_, str):
            from_ = self.scene(from_)
        elif from_ is None:
            from_ = self.most_acc_scene

        def convert_path(path:List[dict]):
            actions = []
            c_path = dict(actions=actions)
            for node in path:
                actions.append(node['action'])

        paths = from_._find_paths(to)

        return paths
