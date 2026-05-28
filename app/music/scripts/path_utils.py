import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATASET_ROOT = os.path.join(PROJECT_ROOT, "datasets", "music")
TRACKS_DIR = os.path.join(PROJECT_ROOT, "tracks")
MODEL_DIR = os.path.join(PROJECT_ROOT, "app/music/trained_models")
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets", "music", "cached_features")