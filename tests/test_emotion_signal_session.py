from app.emotion.signal_session import EmotionSignalSession


def test_initial_session_state_is_off_and_neutral():
    session = EmotionSignalSession()

    assert session.state.fer_status == "Off"
    assert session.state.hr_status == "Off"
    assert session.state.fused_mood == "neutral"
    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": None,
        "combined_mode": False,
        "fused_mood": "neutral",
    }


def test_fer_update_normalizes_label_and_fuses_mood():
    session = EmotionSignalSession()

    session.update_fer(status="Camera active", label="Joy", confidence=0.91)

    assert session.state.fer_status == "Camera active"
    assert session.state.fer_label == "happy"
    assert session.state.fer_confidence == 0.91
    assert session.state.fused_mood == "happy"


def test_hr_update_tracks_bpm_and_label():
    session = EmotionSignalSession()

    session.update_hr(status="Connected", bpm=82, label="Calm")

    assert session.state.hr_status == "Connected"
    assert session.state.bpm == 82
    assert session.state.hr_label == "neutral"
    assert session.state.fused_mood == "neutral"


def test_combined_inputs_mark_combined_mode_when_both_signals_exist():
    session = EmotionSignalSession()

    session.update_fer(status="Camera active", label="happy", confidence=0.8)
    session.update_hr(status="Connected", bpm=126, label="angry")

    assert session.state.fused_mood == "angry"
    assert session.recommendation_inputs() == {
        "fer_emotion": "happy",
        "hr_emotion": "angry",
        "combined_mode": True,
        "fused_mood": "angry",
    }


def test_reset_signal_clears_labels_without_changing_other_signal():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="sad", confidence=0.75)
    session.update_hr(status="Connected", bpm=74, label="neutral")

    session.reset_fer(status="Off")

    assert session.state.fer_status == "Off"
    assert session.state.fer_label is None
    assert session.state.fer_confidence is None
    assert session.state.hr_label == "neutral"
    assert session.state.fused_mood == "neutral"


def test_inactive_status_updates_clear_stale_signal_readings():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="happy", confidence=0.8)
    session.update_hr(status="Connected", bpm=126, label="angry")

    session.update_fer(status="Off")

    assert session.state.fer_status == "Off"
    assert session.state.fer_label is None
    assert session.state.fer_confidence is None
    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": "angry",
        "combined_mode": False,
        "fused_mood": "angry",
    }

    session.update_hr(status="Device not found")

    assert session.state.hr_status == "Device not found"
    assert session.state.hr_label is None
    assert session.state.bpm is None
    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": None,
        "combined_mode": False,
        "fused_mood": "neutral",
    }


def test_omitted_labels_preserve_active_signal_readings():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="happy", confidence=0.8)
    session.update_hr(status="Connected", bpm=96, label="calm")

    session.update_fer(status="Camera active")
    session.update_hr(status="Connected")

    assert session.state.fer_label == "happy"
    assert session.state.fer_confidence == 0.8
    assert session.state.hr_label == "neutral"
    assert session.state.bpm == 96
    assert session.state.fused_mood == "happy"


def test_empty_and_unknown_labels_clear_signal_readings():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="happy", confidence=0.8)

    session.update_fer(status="Camera active", label="   ", confidence=0.5)

    assert session.state.fer_label is None
    assert session.state.fer_confidence is None
    assert session.state.fused_mood == "neutral"

    session.update_fer(status="Camera active", label="confused", confidence=0.4)

    assert session.state.fer_label is None
    assert session.state.fer_confidence is None

    session.update_hr(status="Connected", bpm=101, label="angry")

    session.update_hr(status="Connected", bpm=99, label="")

    assert session.state.hr_label is None
    assert session.state.bpm is None
    assert session.state.fused_mood == "neutral"

    session.update_hr(status="Connected", bpm=88, label="startled")

    assert session.state.hr_label is None
    assert session.state.bpm is None


def test_side_specific_invalid_statuses_become_error_and_clear_signal():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="sad", confidence=0.7)
    session.update_hr(status="Connected", bpm=90, label="happy")

    session.update_fer(status="Connected")

    assert session.state.fer_status == "Error"
    assert session.state.fer_label is None
    assert session.state.fer_confidence is None
    assert session.state.hr_label == "happy"
    assert session.state.fused_mood == "happy"

    session.update_hr(status="No webcam detected")

    assert session.state.hr_status == "Error"
    assert session.state.hr_label is None
    assert session.state.bpm is None
    assert session.state.fused_mood == "neutral"


def test_reset_hr_clears_hr_reading_without_changing_fer_signal():
    session = EmotionSignalSession()
    session.update_fer(status="Camera active", label="sad", confidence=0.75)
    session.update_hr(status="Connected", bpm=92, label="angry")

    session.reset_hr(status="Off")

    assert session.state.hr_status == "Off"
    assert session.state.hr_label is None
    assert session.state.bpm is None
    assert session.state.fer_label == "sad"
    assert session.state.fer_confidence == 0.75
    assert session.state.fused_mood == "sad"


def test_recommendation_inputs_ignore_unavailable_signals():
    session = EmotionSignalSession()

    session.update_fer(status="Model missing")
    session.update_hr(status="Device not found")

    assert session.recommendation_inputs() == {
        "fer_emotion": None,
        "hr_emotion": None,
        "combined_mode": False,
        "fused_mood": "neutral",
    }
