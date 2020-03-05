from dt_automator.maker.model import FeatureModel as MakerFeatureModel
from dt_automator.sdk.model.image import ImageModel


class FeatureModel(MakerFeatureModel):
    def __init__(self):
        super().__init__()
        self.img = ImageModel()
