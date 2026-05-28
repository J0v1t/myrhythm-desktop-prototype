import joblib
import numpy as np
import os
import tensorflow as tf
from typing import Optional, Any
from tensorflow.keras.optimizers import Adam # Import Adam explicitly

# Define paths for the new LSTM model files
# NOTE: These files must be created by running 'train_lstm_model.py'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The Keras model is now saved as a .keras file
MODEL_PATH = os.path.join(BASE_DIR, 'lstm_model.keras')
# The Label Encoder is saved as a separate joblib file
LE_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')

# Global variables to cache the loaded model and encoder for performance
_lstm_model: Optional[tf.keras.Model] = None
_label_encoder: Optional[Any] = None

def load_model_components() -> bool:
    """
    Loads the Keras LSTM model and Label Encoder into memory only once.
    
    This function has been updated to handle the 'Adam' object no attribute 'build'
    error by loading the model without compiling, then manually compiling it.
    
    Returns:
        True if successful, False otherwise.
    """
    global _lstm_model, _label_encoder
    
    if _lstm_model and _label_encoder:
        return True # Already loaded

    try:
        # Load the Keras LSTM model
        # FIX: Use compile=False to bypass the optimizer loading error,
        # then re-compile manually to ensure it is ready for prediction.
        _lstm_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        
        # Manually re-compile the model. We use the same optimizer/loss/metrics
        # as in train_lstm_model.py
        # You must ensure the number of classes matches the expected output shape.
        num_classes = _lstm_model.output_shape[-1]
        
        _lstm_model.compile(
            optimizer=Adam(learning_rate=0.001), 
            loss='sparse_categorical_crossentropy', 
            metrics=['accuracy']
        )
        
        # Load the Label Encoder (joblib is standard for scikit-learn encoders)
        _label_encoder = joblib.load(LE_PATH)
        
        print(f"✅ LSTM Model loaded from {MODEL_PATH}")
        return True
        
    except FileNotFoundError:
        print(f"\nFATAL ERROR: Model files not found. Ensure 'train_lstm_model.py' has been run successfully.")
        print(f"  Missing: {MODEL_PATH} or {LE_PATH}")
        return False
    except Exception as e:
        # The original error ('Adam' object has no attribute 'build') should now be fixed
        # by using compile=False, but we keep a general catch for safety.
        print(f"❌ Error loading model components: {e}")
        # HINT: If the error persists, try updating your TensorFlow version or
        # ensuring the model was saved with a compatible Keras version.
        return False

# Import SEQUENCE_LENGTH for consistency (assuming it's used elsewhere)
try:
    from app.hr.trained_hr_models.hr_feature_engineering import SEQUENCE_LENGTH
except ImportError:
    # Set a fallback default if import fails, but this should be consistent
    SEQUENCE_LENGTH = 10 
    print("Warning: SEQUENCE_LENGTH import failed. Using default=10.")


def predict_emotion_sequence(hr_sequence: np.ndarray) -> str:
    """
    Uses the loaded LSTM model to predict the emotion quadrant from a sequence.
    
    Args:
        hr_sequence: A NumPy array of shape (SEQUENCE_LENGTH, 1) containing filtered HR values.
        
    Returns:
        The predicted emotion quadrant label (e.g., 'High_VA').
    """
    # Ensure components are loaded before predicting
    if not load_model_components():
        return "Model Missing"
    
    global _lstm_model, _label_encoder
    
    try:
        # The model expects a batch dimension: (1, SEQUENCE_LENGTH, 1)
        # This is required by Keras/TensorFlow for prediction
        input_data = np.expand_dims(hr_sequence, axis=0)
        
        # 1. Predict probabilities
        probabilities = _lstm_model.predict(input_data, verbose=0)[0]
        
        # 2. Get the index of the highest probability
        predicted_index = np.argmax(probabilities)
        
        # 3. Decode the index back to the emotional quadrant string
        emotion_label = _label_encoder.inverse_transform([predicted_index])[0]
        
        # Return the label, capitalized for display (e.g., 'high_va' -> 'High_VA')
        return emotion_label.replace('_', ' ').title()
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return "Prediction Error"