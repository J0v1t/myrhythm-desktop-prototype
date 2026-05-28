import os
import json
import joblib
import numpy as np

from feature_extractor import FeatureExtractor
from feature_cache import FeatureCache
from path_utils import PROJECT_ROOT, MODEL_DIR


class MusicEmotionClassifier:

    def __init__(self):
        self.scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
        self.clf = joblib.load(os.path.join(MODEL_DIR, "genre_classifier.pkl"))
        self.le = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

        mapping_path = os.path.join(PROJECT_ROOT, "app", "music", "recommendation", "genre_mapping.json")
        with open(mapping_path, "r") as f:
            self.genre_map = json.load(f)

        self.extractor = FeatureExtractor()
        self.cache = FeatureCache()

    # ---------------------------------------------------------
    # Extract feature vector (prefer DB → fallback to extract)
    # ---------------------------------------------------------
    def get_vector(self, audio_path):
        cached = self.cache.get_features(audio_path)
        if cached:
            data = json.loads(cached.features_json)
            return np.array(data["vector"], dtype=np.float32)
        
        vec = self.extractor.extract_vector(audio_path)
        return np.array(vec, dtype=np.float32)

    # ---------------------------------------------------------
    # Predict genre + emotion
    # ---------------------------------------------------------
    def predict(self, audio_path):
        vec = self.get_vector(audio_path)
        vec_scaled = self.scaler.transform([vec])

        genre_index = self.clf.predict(vec_scaled)[0]
        genre = self.le.inverse_transform([genre_index])[0]

        emotion = self.genre_map.get(genre.lower(), "Neutral")

        return {
            "genre": genre,
            "emotion": emotion
        }
