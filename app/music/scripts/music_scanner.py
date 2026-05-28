import sys
import os

from path_utils import PROJECT_ROOT, TRACKS_DIR
sys.path.insert(0, PROJECT_ROOT)

from feature_extractor import FeatureExtractor
from music_classifier import MusicEmotionClassifier
from feature_cache import FeatureCache
from app.database.schema import SessionLocal
from app.database.models import Song


class MusicScanner:
    """
    Scans a designated music folder, extracts audio features,
    stores metadata + features into the SQLAlchemy database.
    """

    SUPPORTED_FORMATS = (".mp3", ".wav", ".flac", ".ogg", ".m4a")

    def __init__(self, TRACKS_DIR):
        self.music_folder = TRACKS_DIR
        self.extractor = FeatureExtractor()
        self.classifier = MusicEmotionClassifier()
        self.cache = FeatureCache()
        self.db = SessionLocal()

    # -----------------------------------------------------
    # Scan directory for audio files
    # -----------------------------------------------------
    def scan_folder(self):
        print(f"\n📂 Scanning music folder: {self.music_folder}\n")

        if not os.path.exists(self.music_folder):
            print(f"[ERROR] Folder not found: {self.music_folder}")
            return

        for root, _, files in os.walk(self.music_folder):
            for file in files:
                if file.lower().endswith(self.SUPPORTED_FORMATS):
                    file_path = os.path.join(root, file)
                    print(f"🎶 Found audio file: {file_path}")
                    self.process_file(file_path)

        print("\n✔ Scan complete.")

    # -----------------------------------------------------
    # Process a single file (metadata + features)
    # -----------------------------------------------------
    def process_file(self, file_path):
        # Normalize path
        file_path = os.path.abspath(file_path)

        # Check if file exists in DB
        existing = self.db.query(Song).filter_by(file_path=file_path).first()

        # Check cache update requirement
        if existing and not self.cache.needs_update(file_path):
            print("   ↳ Cached version up-to-date. Skipping.")
            return

        print("   ↳ Extracting metadata + features...")
        
        extracted = self.extractor.extract_all(file_path)
        metadata = extracted["metadata"]

        # Classify using DB-cached vector
        result = self.classifier.predict(file_path)

        # fallback defaults
        metadata["title"] = metadata["title"] or os.path.splitext(os.path.basename(file_path))[0]
        metadata["artist"] = metadata["artist"] or "Unknown"
        metadata["genre"] = metadata["genre"] or result["genre"]
        metadata["duration"] = metadata["duration"] or 0

        # Determine cover image path
        cover_path = self.find_cover_path(metadata["title"])

        self.cache.save_features(
            file_path=file_path,
            metadata=metadata,
            feature_dict={"vector": extracted["features"]}
        )

        # Update genre and music cover in DB
        song = self.db.query(Song).filter_by(file_path=file_path).first()
        song.genre = result["genre"]
        song.cover_path = cover_path

        self.db.commit()

        print(f" ✓ Saved ({result['genre']} → {result['emotion']})")

    def find_cover_path(self, title):
        """
        Finds the .webp cover based on song title rules.
        Example: "Wall Of Sound" -> "WallOfSound.webp"
        """
        if not title:
            return None

        normalized = title.replace(" ", "").capitalize()
        cover_name = f"{normalized}.webp"

        cover_path = os.path.join(TRACKS_DIR, "music_cover", cover_name)

        return cover_path if os.path.exists(cover_path) else None


# ---------------------------------------------------------
# Standalone run (python music_scanner.py)
# ---------------------------------------------------------
if __name__ == "__main__":
    scanner = MusicScanner(TRACKS_DIR)
    scanner.scan_folder()
