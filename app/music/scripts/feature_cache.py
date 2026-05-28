import sys
import os

from path_utils import PROJECT_ROOT
sys.path.insert(0, PROJECT_ROOT)

from sqlalchemy.orm import Session
from app.database.schema import SessionLocal
from app.database.models import Song, AudioFeatures
import hashlib
import time
import json


class FeatureCache:
    def __init__(self):
        self.db: Session = SessionLocal()

    # -----------------------------------------------------
    # Hashing utility
    # -----------------------------------------------------
    def compute_hash(self, file_path):
        h = hashlib.sha1()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
    
    # -----------------------------------------------------
    # Return AudioFeatures row OR None
    # -----------------------------------------------------
    def get_features(self, file_path):
        song = self.db.query(Song).filter_by(file_path=file_path).first()
        if not song or not song.audio_features:
            return None
        return song.audio_features

    # -----------------------------------------------------
    # Insert or update song + features
    # -----------------------------------------------------
    def save_features(self, file_path, metadata: dict, feature_dict: dict):
        """
        metadata contains title, artist, duration, genre
        feature_dict contains MFCC, chroma, tempo, etc.
        """

        file_hash = self.compute_hash(file_path)

        # Create or fetch Song row
        song = self.db.query(Song).filter_by(file_path=file_path).first()
        if not song:
            song = Song(
                file_path=file_path,
                title=metadata.get("title"),
                artist=metadata.get("artist"),
                genre=metadata.get("genre"),
                duration=metadata.get("duration"),
            )
            self.db.add(song)
            self.db.commit()
            self.db.refresh(song)

        # Create or update AudioFeatures row
        af = song.audio_features
        if not af:
            af = AudioFeatures(
                song_id=song.id,
                file_hash=file_hash,
                features_json=json.dumps(feature_dict),
                last_scanned=time.time()
            )
            self.db.add(af)
        else:
            af.file_hash = file_hash
            af.features_json = json.dumps(feature_dict)
            af.last_scanned = time.time()

        self.db.commit()

    # -----------------------------------------------------
    # Check if cached features are outdated
    # -----------------------------------------------------
    def needs_update(self, file_path):
        af = self.get_features(file_path)
        if not af:
            return True

        current_hash = self.compute_hash(file_path)

        return af.file_hash != current_hash
    