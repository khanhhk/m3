import json

import constants.vae as vae_constants
import numpy as np
from alibi_detect.saving import load_detector
from loguru import logger

import kserve


# For serializing Numpy arrays
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


class InstrusionDetectionModel(kserve.KFModel):
    def __init__(self, name):
        # The `name` variable is required
        super().__init__(name)
        self.name = name
        self.model = load_detector(vae_constants.WEIGHTS_PATH)

    def predict(self, input_data):
        preds = self.model.predict(
            input_data,
            return_instance_score=vae_constants.RETURN_INSTANCE_SCORE,
            return_feature_score=vae_constants.RETURN_FEATURE_SCORE,
        )
        preds = json.dumps(preds, cls=NumpyArrayEncoder)
        logger.info(preds)
        return preds


if __name__ == "__main__":
    model = InstrusionDetectionModel("intrusion-detection-model")
    kserve.KFServer().start([model])
