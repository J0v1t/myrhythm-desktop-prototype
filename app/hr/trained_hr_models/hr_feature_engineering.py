import numpy as np
import pandas as pd
import os
from typing import List, Tuple, Dict
# Direct imports assuming files are in the same directory
from app.hr.trained_hr_models.kalman_filter import KalmanFilterHR 
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

# --- Configuration ---
# The LSTM model will need a fixed-length sequence of data. 10 samples (seconds) is standard.
SEQUENCE_LENGTH = 10 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: Assuming heart_rate_emotion_dataset.csv is in the same directory as this script.
DATASET_PATH = os.path.join(BASE_DIR, 'heart_rate_emotion_dataset.csv')


# --- Emotional Quadrant Mapping (Based on DEAP-like structure) ---
def map_valence_arousal(valence: float, arousal: float) -> str:
    """
    Maps continuous Valence/Arousal (VA) scores to four distinct quadrants.
    V_MID=5.0 and A_MID=5.0 define the center.
    """
    V_MID = 5.0
    A_MID = 5.0

    if valence > V_MID and arousal > A_MID:
        return "High_VA" # Excited, Happy, Alert (High Valence, High Arousal)
    elif valence <= V_MID and arousal > A_MID:
        return "Low_V_High_A" # Angry, Stressed, Fear (Low Valence, High Arousal)
    elif valence <= V_MID and arousal <= A_MID:
        return "Low_VA" # Sad, Bored, Depressed (Low Valence, Low Arousal)
    else: # valence > V_MID and arousal <= A_MID
        return "High_V_Low_A" # Calm, Relaxed, Content (High Valence, Low Arousal)

def simulate_va_from_hr(hr_value: float) -> Tuple[float, float]:
    """
    Simulates Valence and Arousal scores from a single HR value based on typical ranges.
    
    This is a simplification for classification training:
    - Higher HR implies Higher Arousal (A)
    - HR deviation from resting rate (e.g., 80 BPM) relates to Valence (V)
    
    Arousal is derived from the normalized HR value (e.g., 60=1 to 120=9).
    Valence is kept relatively neutral for most cases, favoring High_V for high HR (Excitement)
    and Low_V for low HR (Sadness/Fear).
    """
    
    # 1. Simulate Arousal (Arousal is highly correlated with HR)
    # Map HR (e.g., 60-120) to Arousal (1.0-9.0)
    min_hr, max_hr = 60.0, 120.0
    min_a, max_a = 1.0, 9.0
    
    # Simple linear scaling: A = (hr - min_hr) * (max_a - min_a) / (max_hr - min_hr) + min_a
    arousal = np.clip((hr_value - min_hr) / (max_hr - min_hr) * (max_a - min_a) + min_a, min_a, max_a)

    # 2. Simulate Valence (more complex, loosely tied to quadrant meaning)
    if hr_value >= 100: # High HR: High Arousal. Valence depends on context: Excitement (High V) or Stress (Low V)
        valence = 7.0 # Assume High V for excitement, pushing to High_VA
    elif hr_value <= 70: # Low HR: Low Arousal. Valence depends on context: Sadness/Boredom (Low V) or Calm (High V)
        valence = 3.0 # Assume Low V, pushing to Low_VA or Low_V_High_A
    else: # Mid range HR (70-100)
        valence = 5.5 # Slightly positive/neutral
        
    return float(valence), float(arousal)


def load_data_and_create_sequences(csv_path: str = DATASET_PATH, sequence_length: int = SEQUENCE_LENGTH) -> Tuple[np.ndarray, np.ndarray, LabelEncoder, KalmanFilterHR]:
    """
    Loads HR data, applies Kalman filtering, simulates VA, maps to emotion quadrants,
    and converts the filtered time series into sequences for LSTM training.

    Returns:
        X (np.ndarray): LSTM input sequences (samples, sequence_length, 1).
        y (np.ndarray): Target labels (encoded integers).
        le (LabelEncoder): The fitted label encoder.
        kf (KalmanFilterHR): The initialized Kalman filter instance.
    """
    print(f"Loading data from: {csv_path}")
    
    # Load the CSV, but only use 'HeartRate' column for the feature
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {csv_path}")
        return np.array([]), np.array([]), LabelEncoder(), KalmanFilterHR()
    
    raw_hr_data = df['HeartRate'].values.tolist()

    # Initialize and apply Kalman Filter to clean the HR stream
    # Initial BPM is set to the first reading or a safe default
    kf = KalmanFilterHR(initial_bpm=raw_hr_data[0] if len(raw_hr_data) > 0 else 80)
    filtered_hr_data = [kf.filter(hr) for hr in raw_hr_data]

    # --- Sequence and Label Creation ---
    X, y_raw = [], []
    
    for i in range(len(filtered_hr_data) - sequence_length + 1):
        # 1. Input Sequence (X): A sliding window of filtered HR values
        hr_sequence = filtered_hr_data[i : i + sequence_length]
        X.append(hr_sequence)
        
        # 2. Output Label (y): Emotion for the *end* of the sequence
        # We use the final HR value in the window to simulate the VA score for the sequence's conclusion
        current_hr = hr_sequence[-1]
        valence, arousal = simulate_va_from_hr(current_hr)
        label = map_valence_arousal(valence, arousal)
        y_raw.append(label)

    if not X:
        print(f"Error: Not enough data to create sequences (sequence_length={sequence_length}).")
        return np.array([]), np.array([]), LabelEncoder(), kf

    X = np.array(X)
    # Reshape X to (samples, sequence_length, 1) for LSTM input
    X = X.reshape(X.shape[0], X.shape[1], 1)
    
    # --- Encoding and Balancing ---
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_raw)
    
    # Reshape X to 2D for SMOTE (temporarily)
    X_smote = X.reshape(X.shape[0], -1) 
    
    # Use SMOTE to balance the classes in the generated emotional quadrants
    smote = SMOTE(random_state=42)
    X_bal_smote, y_bal = smote.fit_resample(X_smote, y_encoded)
    
    # Reshape X back to 3D for LSTM input
    X_bal = X_bal_smote.reshape(X_bal_smote.shape[0], sequence_length, 1)

    print(f"Raw Samples: {len(raw_hr_data)} | Sequences Created: {X.shape[0]}")
    print(f"Balanced Sequences (X shape): {X_bal.shape} | (y shape): {y_bal.shape}")
    print(f"Emotion Classes: {le.classes_}")
    
    # Splitting logic is now moved to train_lstm_model.py
    return X_bal, y_bal, le, kf

if __name__ == "__main__":
    X, y, le, kf = load_data_and_create_sequences()
    if X.size > 0:
        # Example of the first sequence and its label
        print("\nFirst Sequence (Filtered HR values):")
        print(X[0].flatten())
        print(f"Label: {le.inverse_transform([y[0]])[0]}")