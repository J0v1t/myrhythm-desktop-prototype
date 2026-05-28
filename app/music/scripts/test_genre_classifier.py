import os
import joblib

from .feature_extractor import FeatureExtractor
from .path_utils import MODEL_DIR, TRACKS_DIR

songs = []
for filename in os.listdir(TRACKS_DIR):
    file_path = os.path.join(TRACKS_DIR, filename)
    songs.append(file_path)


def test_genre_prediction(audio_path):
    print("\n🎧 Testing genre classifier\n")

    # Load components
    clf = joblib.load(os.path.join(MODEL_DIR, "genre_classifier.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
    le = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

    extractor = FeatureExtractor()

    vec = extractor.extract_vector(audio_path).reshape(1, -1)
    vec_scaled = scaler.transform(vec)

    pred = clf.predict(vec_scaled)[0]
    genre = le.inverse_transform([pred])[0]

    print(f"Track {audio_path} predicted genre:", genre)


if __name__ == "__main__":
    for s in songs:
        if not os.path.exists(s):
            print("❌ TEST_FILE does not exist. Update TEST_FILE path.")
        else:
            test_genre_prediction(s)
