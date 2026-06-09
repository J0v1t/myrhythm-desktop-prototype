import numpy as np
from typing import Optional, Any

from app.config.runtime_assets import resolve_runtime_assets

EMOTION_LABELS = (
    "High_VA",
    "High_V_Low_A",
    "Low_VA",
    "Low_V_High_A",
)
SEQUENCE_LENGTH = 10

# Global variables to cache the loaded model for performance
_lstm_model: Optional[Any] = None
_loaded_model_path: Optional[str] = None


def get_model_artifact_status() -> dict:
    assets = resolve_runtime_assets()
    return {
        "model_path": str(assets.hr_model.path),
        "model_exists": assets.hr_model.exists,
        "ready": assets.hr_model.exists,
    }


def decode_emotion_index(predicted_index: int) -> str:
    """Decode the model's fixed training output order without deserializing code."""
    index = int(predicted_index)
    if index < 0 or index >= len(EMOTION_LABELS):
        raise ValueError(f"Unexpected heart-rate model output index: {index}")
    return EMOTION_LABELS[index].replace("_", " ").title()


def load_model_components() -> bool:
    """
    Loads the Keras LSTM model into memory only once.
    
    This function has been updated to handle the 'Adam' object no attribute 'build'
    error by loading the model without compiling, then manually compiling it.
    
    Returns:
        True if successful, False otherwise.
    """
    global _lstm_model, _loaded_model_path
    
    status = get_model_artifact_status()
    model_path = status["model_path"]
    if _lstm_model and _loaded_model_path == model_path:
        return True # Already loaded

    if not status["ready"]:
        print("\nFATAL ERROR: Model files not found. Ensure 'train_lstm_model.py' has been run successfully.")
        print(f"  Missing: {model_path}")
        return False

    try:
        import tensorflow as tf
        from tensorflow.keras.optimizers import Adam

        # Load the Keras LSTM model
        # FIX: Use compile=False to bypass the optimizer loading error,
        # then re-compile manually to ensure it is ready for prediction.
        _lstm_model = tf.keras.models.load_model(model_path, compile=False)
        
        # Manually re-compile the model. We use the same optimizer/loss/metrics
        # as in train_lstm_model.py
        # You must ensure the number of classes matches the expected output shape.
        num_classes = _lstm_model.output_shape[-1]
        
        _lstm_model.compile(
            optimizer=Adam(learning_rate=0.001), 
            loss='sparse_categorical_crossentropy', 
            metrics=['accuracy']
        )
        
        _loaded_model_path = model_path
        
        print(f"✅ LSTM Model loaded from {model_path}")
        return True
        
    except FileNotFoundError:
        print(f"\nFATAL ERROR: Model files not found. Ensure 'train_lstm_model.py' has been run successfully.")
        print(f"  Missing: {model_path}")
        return False
    except Exception as e:
        # The original error ('Adam' object has no attribute 'build') should now be fixed
        # by using compile=False, but we keep a general catch for safety.
        print(f"❌ Error loading model components: {e}")
        # HINT: If the error persists, try updating your TensorFlow version or
        # ensuring the model was saved with a compatible Keras version.
        return False

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
    
    global _lstm_model
    
    try:
        # The model expects a batch dimension: (1, SEQUENCE_LENGTH, 1)
        # This is required by Keras/TensorFlow for prediction
        input_data = np.expand_dims(hr_sequence, axis=0)
        
        # 1. Predict probabilities
        probabilities = _lstm_model.predict(input_data, verbose=0)[0]
        
        # 2. Get the index of the highest probability
        predicted_index = np.argmax(probabilities)
        
        # 3. Decode the index back to the emotional quadrant string
        return decode_emotion_index(predicted_index)
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return "Prediction Error"
