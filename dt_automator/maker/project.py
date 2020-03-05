import json
import os
from typing import Dict

from dt_automator.maker.model import SceneModel


class Project:
    FILENAME_INFO = 'info.json'

    def __init__(self):
        self._path = None
        self._event = dict(
            get_path=self.get_path,
        )
        self.scenes = {}  # type: Dict[SceneModel]

    @staticmethod
    def open(path):
        if os.path.exists(path) and os.path.isdir(path):
            self = Project()
            self._path = path
            if os.path.exists('%s/%s' % (path, self.FILENAME_INFO)):
                self.load()
            return self

    def load(self):
        path = self.get_path(self.FILENAME_INFO)
        with open(path, encoding='utf-8') as io:
            data = json.load(io)  # type: dict
        items = {}
        for k, v in data.items():
            scene = SceneModel(self._event)
            scene.load_data(**v)
            items[k] = scene
        self.scenes = items

    def get_path(self, filename, create_dir=False):
        path = '%s/%s' % (self._path, filename)
        if create_dir:
            dir_ = os.path.dirname(path)
            os.makedirs(dir_, exist_ok=True)
        return path
