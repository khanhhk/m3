from abc import ABC, abstractmethod
from sklearn.metrics import confusion_matrix, f1_score
from alibi_detect.saving import save_detector, load_detector
from .model import initialize_vae, initialize_isf

SUPPORTED_METRICS = [
    "f1_score"
]

SUPPORTED_MODELS = [
    "vae",
    "isf"
]

class Trainer(object):
    """
    Base class for all trainers
    """
    def __init__(self, model_name="vae", *args, **kwargs):
        self.model_name = model_name.lower()
        if model_name in SUPPORTED_MODELS:
            self.model = eval(f"initialize_{model_name}(*args, **kwargs)")
        else:
            raise ValueError(f"Unsupported model {model_name} for Trainer!")
        
    def train(self, X_train, perc_outlier, *args, **kwargs):
        self.model.fit(X_train, *args, **kwargs)
        
        # Infer outlier threshold
        self.model.infer_threshold(X_train, threshold_perc=100-perc_outlier)
        
    def load_model(self, filepath):
        self.model = load_detector(filepath)
        
    def predict(self, X_test, *args, **kwargs):
        return self.model.predict(X_test, *args, **kwargs)
        
    @staticmethod
    def evaluate(y_test, y_pred, metric="f1_score"):
        if metric in SUPPORTED_METRICS:
            score = eval(f"{metric}(y_test, y_pred)")
            return score
        else:
            raise ValueError(f"Metric {metric} is not supported!")

    def save_model(self, filepath):
        save_detector(self.model, filepath)