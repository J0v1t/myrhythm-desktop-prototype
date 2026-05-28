import os
import joblib
import pandas as pd
import numpy as np
from tqdm import tqdm
import traceback

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

from .feature_extractor import FeatureExtractor
from .path_utils import MODEL_DIR, DATASET_ROOT

FMA_AUDIO_DIR = os.path.join(DATASET_ROOT, "fma_small")        # adjust if needed
FMA_METADATA = os.path.join(DATASET_ROOT, "fma_metadata", "tracks.csv") 

os.makedirs(MODEL_DIR, exist_ok=True)


def fma_audio_path(track_id):
    """
    FMA stores files like:
        fma_small/123/123456.mp3
    """
    tid_str = f"{int(track_id):06d}"  # zero-pad to 6 digits
    folder = tid_str[:3]
    file_name = f"{tid_str}.mp3"
    return os.path.join(FMA_AUDIO_DIR, folder, file_name)


def train_genre_classifier(max_examples=None, debug=False):

    print("Loading FMA metadata...")
    meta = pd.read_csv(FMA_METADATA, header=[0, 1], index_col=0, low_memory=False)

    if ('set', 'subset') not in meta.columns or ('track', 'genre_top') not in meta.columns:
        raise RuntimeError("tracks.csv does not contain expected multiindex columns ('set','subset') or ('track','genre_top').")
    
    # Only keep rows in the "small" subset
    small = meta[meta[('set', 'subset')] == 'small'].copy()
    small = small[small[('track', 'genre_top')].notna()].copy()

    print("Total tracks in metadata :", len(meta))
    print("Tracks in 'small' subset  :", len(small))

    # Build list of (track_id, genre)
    rows = []
    for idx, row in small.iterrows():
        try:
            track_id = int(idx)
            genre = row[('track', 'genre_top')]
            if pd.isna(genre):
                genre = "unknown"
            rows.append((track_id, str(genre)))
        except Exception:
            continue

    if max_examples:
        rows = rows[:max_examples]

    extractor = FeatureExtractor()

    X = []
    y = []
    skipped = 0
    total = len(rows)

    print(f"Attempting to process {total} tracks... (this may take a while)")
   
    for track_id, genre in tqdm(rows):
        file_path = fma_audio_path(track_id)
        if file_path is None or not os.path.exists(file_path):
            skipped += 1
            continue

        try:
            vec = extractor.extract_vector(file_path)
            if vec is None:
                skipped += 1
                continue
            X.append(vec)
            y.append(genre)
        except Exception as e:
            skipped += 1
            if debug:
                print("Error processing", file_path)
                traceback.print_exc()
            continue

    if len(X) == 0:
        raise RuntimeError("No audio features extracted. Check that FMA files exist and extractor works.")

    X = np.vstack(X)
    y = np.array(y)

    print(f"Feature matrix shape: {X.shape}; Labels: {y.shape}; skipped: {skipped}")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Label encoder
    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    print("Training RandomForest genre classifier...")
    clf = RandomForestClassifier(n_estimators=300, n_jobs=-1, random_state=42)
    clf.fit(X_scaled, y_enc)

    # Save models
    joblib.dump(clf, os.path.join(MODEL_DIR, "genre_classifier.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    print("Genre classifier training complete!")
    print("Saved to:", MODEL_DIR)


if __name__ == "__main__":
    train_genre_classifier(max_examples=None, debug=False)
