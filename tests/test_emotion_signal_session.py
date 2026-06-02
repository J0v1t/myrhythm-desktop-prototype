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
    assert session.state.hr_label == "neutral"
    assert session.state.fused_mood == "neutral"
