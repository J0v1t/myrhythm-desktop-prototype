import os
import joblib
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
# Direct imports
from app.hr.trained_hr_models.hr_feature_engineering import load_data_and_create_sequences, SEQUENCE_LENGTH
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical # Not explicitly used for sparse, but kept
from tensorflow.keras.optimizers import Adam # Ensure Adam is imported explicitly

# Define paths (assuming the model will be saved in the same directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'lstm_model.keras') # Use the recommended .keras format
LE_PATH = os.path.join(BASE_DIR, 'label_encoder.pkl')

def build_lstm_model(sequence_length: int, num_classes: int) -> tf.keras.Model:
    """Builds the Keras LSTM model for sequence classification."""
    
    # --- LSTM Model Architecture --- 
    model = Sequential([
        # LSTM layer to capture temporal dependencies in the N-sample sequence
        # input_shape is (time_steps, features) -> (SEQUENCE_LENGTH, 1)
        LSTM(units=64, input_shape=(sequence_length, 1), return_sequences=False, name='lstm_layer'),
        Dropout(0.3),
        # Dense layers for final classification
        Dense(32, activation='relu', name='dense_1'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax', name='output_layer') # Softmax for multi-class classification
    ])
    
    # Use Sparse Categorical Crossentropy because our labels are single integers (not one-hot encoded)
    # The Adam optimizer is explicitly called here
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_and_save_model():
    """Main function to load data, train the model, and save components."""
    
    # 1. Load Data
    X, y_encoded, le, _ = load_data_and_create_sequences()
    
    if X.size == 0:
        print("🛑 Data loading failed or resulted in zero sequences. Training cancelled.")
        return
        
    num_classes = len(le.classes_)
    print(f"Total emotion classes found: {num_classes}")
    
    # 1a. Save the label encoder
    joblib.dump(le, LE_PATH)
    print(f"\n✅ Label Encoder saved at {LE_PATH}. Classes: {le.classes_}")

    # 2. Split Data
    # Use stratify to ensure all 4 emotion quadrants are represented proportionally in train/test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    print(f"Train samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}")

    # 3. Build and Train Model
    model = build_lstm_model(SEQUENCE_LENGTH, num_classes)
    
    print("\n--- Starting LSTM Model Training ---")
    
    # Use EarlyStopping to prevent overfitting
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=10, restore_best_weights=True
    )
    
    history = model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=32,
        validation_data=(X_test, y_test),
        callbacks=[early_stopping],
        verbose=1
    )
    print("--- Training Complete ---")

    # 4. Evaluate and Save
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nModel Test Loss: {loss:.4f} | Model Test Accuracy: {accuracy*100:.2f}%")
    
    # Save the model in the native Keras format (.keras)
    model.save(MODEL_PATH) 
    print(f"✅ LSTM Model saved at {MODEL_PATH}")
    
    # Also save the training history (optional, for debugging/analysis)
    # joblib.dump(history.history, os.path.join(BASE_DIR, 'training_history.pkl'))


if __name__ == "__main__":
    train_and_save_model()