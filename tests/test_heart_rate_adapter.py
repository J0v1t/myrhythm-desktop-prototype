from app.hr.scripts.ble_reader import parse_hr_measurement
from app.hr.trained_hr_models.classifier import get_model_artifact_status


def test_parse_hr_measurement_reads_uint8_payload():
    assert parse_hr_measurement(bytearray([0x00, 72])) == 72


def test_parse_hr_measurement_reads_uint16_payload():
    assert parse_hr_measurement(bytearray([0x01, 0x2C, 0x01])) == 300


def test_parse_hr_measurement_returns_none_for_empty_payload():
    assert parse_hr_measurement(bytearray()) is None


def test_parse_hr_measurement_returns_none_for_incomplete_uint16_payload():
    assert parse_hr_measurement(bytearray([0x01, 0x2C])) is None


def test_hr_model_artifact_status_uses_runtime_assets(monkeypatch, tmp_path):
    model = tmp_path / "lstm_model.keras"
    encoder = tmp_path / "label_encoder.pkl"
    model.write_text("model", encoding="utf-8")
    encoder.write_text("encoder", encoding="utf-8")
    monkeypatch.setenv("MYRHYTHM_HR_MODEL_PATH", str(model))
    monkeypatch.setenv("MYRHYTHM_HR_LABEL_ENCODER_PATH", str(encoder))

    status = get_model_artifact_status()

    assert status["model_path"] == str(model)
    assert status["label_encoder_path"] == str(encoder)
    assert status["model_exists"] is True
    assert status["label_encoder_exists"] is True
    assert status["ready"] is True
