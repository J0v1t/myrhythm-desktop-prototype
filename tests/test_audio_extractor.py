import sys
import os
import pytest

# Add the parent directory to sys.path to allow importing from 'app'
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

pytest.importorskip("librosa")
pytest.importorskip("mutagen")
pytest.importorskip("numpy")

from app.music.scripts.audio_feature_extractor import AudioFeatureExtractor

def test_audio_feature_extraction_with_local_sample():
    sample_path = os.environ.get("MYRHYTHM_SAMPLE_AUDIO")
    if not sample_path or not os.path.exists(sample_path):
        pytest.skip("Set MYRHYTHM_SAMPLE_AUDIO to a licensed local audio file to run this test.")

    extractor = AudioFeatureExtractor()
    result = extractor.extract_all(sample_path)

    assert "metadata" in result
    assert "features" in result
    assert result["features"]
