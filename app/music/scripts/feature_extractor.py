import librosa
import numpy as np
from mutagen import File as MutagenFile

import librosa.feature.rhythm

class FeatureExtractor:
    """
    Unified audio feature extractor used for:
    - training (FMA)
    - music classifier
    - music scanner
    """

    def __init__(self, sr=22050, n_mfcc=13):
        self.sr = sr
        self.n_mfcc = n_mfcc

    # ---------------------------------------------------------
    # Extract metadata using mutagen
    # ---------------------------------------------------------
    def extract_metadata(self, file_path):
        audio = MutagenFile(file_path, easy=True)

        title = None
        artist = None
        genre = None

        if audio is not None:
            title = audio.tags.get("title", [None])[0] if audio.tags else None
            artist = audio.tags.get("artist", [None])[0] if audio.tags else None
            genre = audio.tags.get("genre", [None])[0] if audio.tags else None

        # Duration
        duration = audio.info.length if audio and audio.info else 0

        return {
            "title": title,
            "artist": artist,
            "genre": genre,
            "duration": duration
        }

    def extract_vector(self, file_path):
        y, sr = librosa.load(file_path, sr=self.sr, mono=True)

        if y is None or y.size == 0:
            raise RuntimeError(f"Failed to load audio: {file_path}")

        # MFCC
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_var = np.var(mfcc, axis=1)

        # Chroma
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)

        # Spectral features
        centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
        rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))

        # Tempo
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = float(librosa.feature.
        rhythm.tempo(onset_envelope=onset_env, sr=sr)[0])

        rms = float(np.mean(librosa.feature.rms(y=y)))

        # Final vector
        vec = np.concatenate([
            mfcc_mean,            # 13
            mfcc_var,             # 13
            chroma_mean,          # 12
            np.array([centroid, bandwidth, rolloff, tempo, rms], dtype=np.float32)
        ])

        return vec.astype(np.float32)
    
    # ---------------------------------------------------------
    # Extract everything together (metadata + features)
    # ---------------------------------------------------------
    def extract_all(self, file_path):
        try:
            metadata = self.extract_metadata(file_path)
            vector = self.extract_vector(file_path)
        except Exception as e:
            print(f"   ⚠ Metadata/feature extraction failed: {e}")
            return None

        return {
            "metadata": metadata,
            "features": vector.tolist()
        }
