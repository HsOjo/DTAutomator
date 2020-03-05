import json
from typing import Dict

from PIL.Image import open as img_open, Image

from dt_automator.maker import Project
from dt_automator.maker.model import SceneModel as MakerSceneModel
from dt_automator.sdk.model import SceneModel, ObjectModel, FeatureModel


class DTAutomator:
    def __init__(self):
        self.scenes = {}  # type: Dict[SceneModel]

    def load_from_maker(self, path_dir: str):
        project = Project.open(path_dir)
        scenes = {}
        for name, scene in project.scenes.items():
            scene: MakerSceneModel
            io_img = open(scene.img_path, 'rb')
            img = img_open(io_img)  # type:Image
            new_scene = SceneModel()
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
        with open(path, 'r', encoding='utf-8') as io:
            data = json.load(io)  # type: dict
        scenes = {}
        for k, v in data.items():
            scene = SceneModel()
            scene.load_data(**v)
            scenes[k] = scene
        self.scenes = scenes

    def dump(self, path):
        data = dict((k, v.data) for k, v in self.scenes.items())
        data_str = json.dumps(data, ensure_ascii=False)
        with open(path, 'w', encoding='utf-8') as io:
            io.write(data_str)
