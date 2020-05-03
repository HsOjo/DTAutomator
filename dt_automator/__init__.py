import json
import time
import zlib
from io import BytesIO
from threading import Thread
from typing import Dict

from PIL.Image import open as img_open, Image
from pyadb import Device
from pyandroidtouch import PyAndroidTouchADB

import dt_automator.sdk.model as M
from dt_automator.maker import Project
from dt_automator.maker.model import MakerSceneModel


class StopException(Exception):
    pass


class DTAutomator:
    def __init__(self, device: Device = None, refresh_interval=100):
        self._scenes = {}  # type: Dict[str, M.SceneModel]
        self._event = dict(
            get_scenes=lambda: self._scenes
        )

        self._refresh_interval = refresh_interval / 1000
        self._device = None  # type: Device
        self._pat = None  # type: PyAndroidTouchADB

        self._is_pause = False
        self._is_stop = True

        if device is not None:
            self.set_device(device)

    def _callback_action_update(self):
        while self._is_pause:
            time.sleep(self._refresh_interval)
        if self._is_stop:
            raise StopException()

    def _callback_thread(self):
        self._is_pause = False
        self._is_stop = False

        self.callback_init()
        while not self._is_stop:
            while self._is_pause and not self._is_stop:
                time.sleep(self._refresh_interval)
            if self._is_stop:
                break

            try:
                self.callback_update()
            except StopException:
                break

            time.sleep(self._refresh_interval)
        self.callback_destroy()

    def callback_init(self):
        pass

    def callback_update(self):
        pass

    def callback_destroy(self):
        pass

    def callback_screen_update(self, img_data: bytes):
        pass

    def callback_scenes_update(self, most_acc_scene: M.SceneModel):
        pass

    def play(self):
        if self._is_pause:
            self._is_pause = False
        elif self._is_stop:
            Thread(target=self._callback_thread).start()

    def pause(self):
        self._is_pause = True

    def stop(self):
        self._is_stop = True

    def load_from_maker(self, path_dir: str):
        project = Project.open(path_dir)
        scenes = {}
        for name, scene in project.scenes.items():
            scene: MakerSceneModel
            io_img = open(scene.img_path, 'rb')
            img = img_open(io_img)  # type: Image
            new_scene = M.SceneModel(self._event)
            new_scene.name = scene.name
            for feature in scene.features:
                new_feature = M.FeatureModel()
                new_feature.load_data(**feature.data)
                new_feature.img.load_image(img, *feature.rect)
                new_scene.features.append(new_feature)
            for object_ in scene.objects:
                new_object = M.ObjectModel()
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
            scene = M.SceneModel(self._event)
            scene.load_data(**v)
            scenes[k] = scene
        self._scenes = scenes

    def dump(self, path):
        data = dict((k, v.data) for k, v in self._scenes.items())
        data_str = json.dumps(data, ensure_ascii=False)
        data = zlib.compress(data_str.encode('utf-8'))
        with open(path, 'wb') as io:
            io.write(data)

    def set_device(self, device: Device):
        self._device = device
        self._pat = PyAndroidTouchADB(device)
        self._pat.set_callback_action_begin(lambda *_: self._callback_action_update())
        self._pat.set_callback_action_end(lambda *_: self._callback_action_update())

    def compare_scenes(self, img_data=None):
        if img_data is None:
            img_data = self.screen
        io_img = BytesIO(img_data)
        img = img_open(io_img)
        for scene in self._scenes.values():
            scene.compare(img)
        io_img.close()

        most_acc_scene = self.most_acc_scene
        self.callback_scenes_update(most_acc_scene)

        return most_acc_scene

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
        screen = self._device.display.screen_cap()
        self.callback_screen_update(screen)
        return screen

    def find_paths(self, to, from_=None):
        if isinstance(to, str):
            to = self.scene(to)
        if to is None:
            return None
        if isinstance(from_, str):
            from_ = self.scene(from_)
        elif from_ is None:
            from_ = self.most_acc_scene

        paths = from_.find_paths(to)
        return paths

    def do_path_actions(self, path: M.PathModel, detect_always=False, detect_timeout=10, detect_finish=True):
        begin_time = time.time()

        def hook_did_action(node: M.PathNodeModel):
            if detect_always:
                while True:
                    self.compare_scenes()
                    if self.most_acc_scene != node.dest_scene:
                        if time.time() - begin_time > detect_timeout:
                            return False
                    else:
                        break
            return True

        result = path.do_actions(self._pat, hook_did_action)
        if detect_finish and not detect_always:
            self.compare_scenes()
            return path[-1].dest_scene == self.most_acc_scene

        return result

    def destroy(self):
        if self._pat is not None:
            self._pat.destroy()

    @property
    def device(self):
        return self._device

    @property
    def pyandroidtouch(self):
        return self._pat
