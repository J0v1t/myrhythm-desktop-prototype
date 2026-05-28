import librosa
import numpy as np
from mutagen import File as MutagenFile
import os


class AudioFeatureExtractor:
    """
    Extracts audio features (MFCC, chroma, tempo, spectral features)
    from local audio files using librosa.
    """

    def __init__(self, sr=22050, n_mfcc=20):
        self.sr = sr
        self.n_mfcc = n_mfcc

    # ---------------------------------------------------------
    # Load audio file and return y (waveform) and sr (sample rate)
    # ---------------------------------------------------------
    def load_audio(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            y, sr = librosa.load(file_path, sr=self.sr, mono=True)
            return y, sr
        except Exception as e:
            print(f"[ERROR] Failed to load {file_path}: {e}")
            return None, None

    # ---------------------------------------------------------
    # Extract metadata using Mutagen
    # ---------------------------------------------------------
    def get_audio_metadata(self, file_path):
        try:
            audio = MutagenFile(file_path)
            if not audio:
                return {}

            metadata = {
                "title": audio.tags.get("TIT2").text[0] if audio.tags and "TIT2" in audio.tags else None,
                "artist": audio.tags.get("TPE1").text[0] if audio.tags and "TPE1" in audio.tags else None,
                "genre": audio.tags.get("TCON").text[0] if audio.tags and "TCON" in audio.tags else None,
                "duration": audio.info.length if audio.info else None,
            }

            return metadata

        except Exception as e:
            print(f"[WARNING] Metadata extraction failed for {file_path}: {e}")
            return {}

    # ---------------------------------------------------------
    # Extract features from audio using librosa
    # ---------------------------------------------------------
    def extract_features(self, file_path):
        y, sr = self.load_audio(file_path)

        if y is None:
            return None  # File failed to load

        features = {}

        # ------------------------ MFCC ------------------------
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        features["mfcc_mean"] = np.mean(mfcc, axis=1).tolist()
        features["mfcc_var"] = np.var(mfcc, axis=1).tolist()

        # ------------------------ Chroma ------------------------
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features["chroma_mean"] = np.mean(chroma, axis=1).tolist()

        # ------------------------ Spectral Features ------------------------
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

        features["spectral_centroid"] = float(np.mean(spectral_centroid))
        features["spectral_bandwidth"] = float(np.mean(spectral_bandwidth))
        features["spectral_contrast"] = np.mean(spectral_contrast, axis=1).tolist()
        features["spectral_rolloff"] = float(np.mean(spectral_rolloff))

        # ------------------------ Tempo & Beat ------------------------
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        features["tempo"] = float(tempo)

        # Beat strength (energy of beats)
        features["beat_strength"] = float(np.mean(librosa.onset.onset_strength(y=y, sr=sr)))

        # ------------------------ RMS Energy ------------------------
        rms = librosa.feature.rms(y=y)
        features["rms_energy"] = float(np.mean(rms))

        return features

    # ---------------------------------------------------------
    # Full extraction pipeline: metadata + audio features
    # ---------------------------------------------------------
    def extract_all(self, file_path):
        metadata = self.get_audio_metadata(file_path)
        features = self.extract_features(file_path)

        if features is None:
            return None

        return {
            "metadata": metadata,
            "features": features
        }
