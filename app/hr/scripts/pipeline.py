import numpy as np
from typing import List, Tuple
import statistics
import os
import sys

# Define the directory where the final emotion summary will be saved
# Assumes the script runs from the project root or a directory above 'hr'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Direct imports from local files
try:
    from app.hr.trained_hr_models.kalman_filter import KalmanFilterHR
    from app.hr.trained_hr_models.classifier import predict_emotion_sequence, load_model_components
    from app.hr.trained_hr_models.hr_feature_engineering import SEQUENCE_LENGTH
except ImportError as e:
    print(f"❌ Error during import: {e}")
    sys.exit(1)

# --- Pipeline State Variables ---
_kalman_filter = KalmanFilterHR(initial_bpm=80.0) 
_hr_history: List[float] = []
# NEW: History of predicted emotions (for final mode calculation)
_emotion_history: List[str] = [] 

# Ensure the model is loaded when the module initializes
load_model_components()

def map_quadrant_to_emotion(quadrant_label: str) -> str:
    """
    Maps the predicted Valence/Arousal (VA) quadrant label to a primary emotion 
    (Happy, Neutral, Sad, Angry) using the standard rule-based system.
    """
    # Standard Russell's Circumplex Model Mapping:
    
    # 1. High Valence, High Arousal (Excitement/Joy) -> Happy
    if quadrant_label == 'High Va':
        return "Happy"
    
    # 2. Low Valence, Low Arousal (Sadness/Depression) -> Sad
    elif quadrant_label == 'Low Va':
        return "Sad"
    
    # 3. High Valence, Low Arousal (Calmness/Relaxation) -> Neutral
    elif 'High V Low A' in quadrant_label:
        return "Neutral"
    
    # 4. Low Valence, High Arousal (Anxiety/Tension) -> Angry
    elif 'Low V High A' in quadrant_label:
        return "Angry"
        
    else:
        return "N/A"

def get_current_filtered_bpm() -> float:
    """Returns the most recent filtered BPM value."""
    return _kalman_filter.get_current_estimate() 

def calculate_final_emotion_and_save():
    """
    Calculates the final emotion (mode of the history) and saves it to a file.
    This function is called by real_time_emotion_monitor.py upon shutdown.
    """
    if not _emotion_history:
        final_emotion = "N/A (No prediction data recorded)"
    else:
        # Use mode (most frequent) emotion as the final result
        try:
            final_emotion = statistics.mode(_emotion_history)
        except statistics.StatisticsError:
            # Handle cases where multiple emotions occur with the same highest frequency
            final_emotion = f"Tie detected (First element): {_emotion_history[0]}"
    
    # Ensure the directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    file_path = os.path.join(DATA_DIR, 'final_emotion.txt')
    
    with open(file_path, 'w') as f:
        f.write(f"Final Emotion (Mode): {final_emotion}\n")
        f.write(f"Total Prediction Samples: {len(_emotion_history)}\n")
        
    
    
    # Reset history after saving
    _emotion_history.clear()


def predict_emotions_live(bpm_value: int) -> Tuple[str, str]:
    """
    Processes a new raw BPM value, applies the override rule, and runs the LSTM prediction.
    """
    if not isinstance(bpm_value, int) or bpm_value <= 0:
        return "Invalid Input", "Invalid Input"
        
    # 1. Apply Kalman Filter & Update HR History
    filtered_bpm = _kalman_filter.filter(float(bpm_value))
    _hr_history.append(filtered_bpm)
    
    # Trim the buffer
    if len(_hr_history) > SEQUENCE_LENGTH:
        _hr_history.pop(0) 

    # 2. Check for Sequence Readiness (This takes precedence)
    if len(_hr_history) < SEQUENCE_LENGTH:
        return "Buffering Data", "Buffering Data" 
        
    # --- 3. HARD-CODED RULE: Force ANGRY if Raw BPM > 125 ---
    if bpm_value > 125:
        predicted_quadrant = "Low V High A"
        primary_emotion = "Angry"
        
    else:
        # --- 4. Original LSTM Prediction ---
        hr_sequence_array = np.array(_hr_history).reshape(SEQUENCE_LENGTH, 1)
        predicted_quadrant = predict_emotion_sequence(hr_sequence_array)
        primary_emotion = map_quadrant_to_emotion(predicted_quadrant)
    
    # --- 5. Store Emotion History ---
    if primary_emotion not in ["Buffering Data", "N/A", "Invalid Input"]:
        _emotion_history.append(primary_emotion)
    
    return predicted_quadrant, primary_emotion