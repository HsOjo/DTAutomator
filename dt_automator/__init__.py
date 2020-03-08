import json
import zlib
from io import BytesIO
from typing import Dict

from PIL.Image import open as img_open, Image
from pyadb import Device

from dt_automator.maker import Project
from dt_automator.maker.model import SceneModel as MakerSceneModel
from dt_automator.sdk.model import SceneModel, ObjectModel, FeatureModel


class DTAutomator:
    def __init__(self, device: Device):
        self.scenes = {}  # type: Dict[str, SceneModel]
        self._event = dict(
            get_scenes=lambda: self.scenes
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
        self.scenes = scenes

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
        self.scenes = scenes

    def dump(self, path):
        data = dict((k, v.data) for k, v in self.scenes.items())
        data_str = json.dumps(data, ensure_ascii=False)
        data = zlib.compress(data_str.encode('utf-8'))
        with open(path, 'wb') as io:
            io.write(data)

    @property
    def current_scene(self):
        img_data = self._device.display.screen_cap()
        io_img = BytesIO(img_data)
        img = img_open(io_img)
        current_scene = None  # type: SceneModel
        mp = 0
        for scene in self.scenes.values():
            p = scene.compare(img)
            if p > 0.8:
                print(scene.name, p)
                if p > mp:
                    mp = p
                    current_scene = scene

        io_img.close()
        return current_scene
