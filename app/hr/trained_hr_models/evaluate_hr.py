import os
import joblib
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
# Removed unused matplotlib.pyplot and seaborn
from sklearn.model_selection import train_test_split
from typing import Tuple, Any
import pandas as pd # <-- Added pandas for clean matrix display
import sys

# --- Import Core Components for Data Loading ---
try:
    from app.hr.trained_hr_models.hr_feature_engineering import load_data_and_create_sequences, SEQUENCE_LENGTH
    # We use path constants defined in classifier.py
    from app.hr.trained_hr_models.classifier import MODEL_PATH, LE_PATH 
except ImportError as e:
    print(f"❌ Error during import: {e}")
    print("Ensure all required files (hr_feature_engineering.py, classifier.py) are present.")
    sys.exit(1)

# --- Evaluation Functions ---

def load_evaluation_data() -> Tuple[np.ndarray, np.ndarray, Any]:
    """
    Loads and preprocesses the HR dataset, then splits it into training and testing sets.
    
    Returns:
        A tuple (X_test, y_test, label_encoder) or exits on failure.
    """
    print("--- 1. Loading and Preprocessing Data ---")
    
    # Load data, create LSTM sequences, encode labels, and perform SMOTE balancing.
    X, y_encoded, le, _ = load_data_and_create_sequences() 
    
    if X.size == 0:
        print("🛑 Data loading failed or resulted in zero sequences.")
        sys.exit(1)
        
    # Re-create the 80/20 train/test split using the SMOTE-balanced data (as done in train_lstm_model.py)
    # This ensures consistency in evaluation.
    _, X_test, _, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"Evaluation Test Samples: {X_test.shape[0]}")
    return X_test, y_test, le

def evaluate_model(X_test: np.ndarray, y_test: np.ndarray, label_encoder: Any):
    """
    Loads the trained model, makes predictions, and prints the classification results and confusion matrix.
    
    Args:
        X_test: Test feature sequences (3D NumPy array).
        y_test: True labels for the test set (1D NumPy array).
        label_encoder: The LabelEncoder instance used to decode labels.
    """
    print("\n--- 2. Loading Model and Encoder ---")
    try:
        # Load the Keras LSTM model
        model = tf.keras.models.load_model(MODEL_PATH)
    except Exception as e:
        print(f"🛑 Error loading model from {MODEL_PATH}: {e}")
        print("   -> Ensure 'train_lstm_model.py' was run successfully.")
        return
    
    # --- Prediction ---
    print("\n--- 3. Running Predictions and Evaluation ---")
    
    # Predict probabilities for the test set
    y_pred_probs = model.predict(X_test, verbose=0)
    
    # Get the index of the class with the highest probability
    y_pred_encoded = np.argmax(y_pred_probs, axis=1)
    
    # Decode the numerical labels back to string names for the report
    target_names = label_encoder.classes_
    y_true_labels = label_encoder.inverse_transform(y_test)
    y_pred_labels = label_encoder.inverse_transform(y_pred_encoded)
    
    # --- Classification Report ---
    print("\n[Classification Report]")
    print(classification_report(y_true_labels, y_pred_labels, target_names=target_names))
    
    # --- Confusion Matrix (Console Output) ---
    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=target_names)
    
    # Convert to a DataFrame for a clean, labeled display
    cm_df = pd.DataFrame(cm, index=target_names, columns=target_names)
    
    print("\n[Confusion Matrix (Rows=True Label, Columns=Predicted Label)]")
    print(cm_df)

if __name__ == "__main__":
    print("--- LSTM Model Evaluation Script ---")
    
    # Check if model files exist
    if not os.path.exists(MODEL_PATH) or not os.path.exists(LE_PATH):
        print(f"🛑 Error: Model or Encoder files not found.")
        print("   -> Run 'train_lstm_model.py' first to create these files.")
        sys.exit(1)

    # 1. Load Data
    X_test, y_test, label_encoder = load_evaluation_data()
    
    # 2. Evaluate Model
    evaluate_model(X_test, y_test, label_encoder)