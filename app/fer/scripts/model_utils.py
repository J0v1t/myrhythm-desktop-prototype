from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from deepface import DeepFace

def build_finetuned_fer_model(num_classes=4, dropout_rate=0.5):
    """
    Loads DeepFace Emotion base model and builds a classification head.
    Returns tuple: (model, base_model)
      - model: full Model (base input -> new head output)
      - base_model: the original DeepFace base Keras model (useful for unfreezing)
    Notes:
      - By default, all base_model layers are frozen. Unfreeze when fine-tuning.
      - Uses GlobalAveragePooling2D instead of Flatten for stability.
    """
    # Load DeepFace Emotion model
    base_wrapper = DeepFace.build_model(
        task="facial_attribute", 
        model_name="Emotion"
    )
    base_model = base_wrapper.model  # Extract Keras model

    # Remove the final 7-class softmax layer
    # (We take the layer BEFORE the softmax)
    feature_output = base_model.layers[-2].output

    # Replace it with our own classifier head
    x = feature_output

    try:
        # If tensor has spatial dims, this will work
        x = GlobalAveragePooling2D()(x)
    except Exception:
        # If it's already flattened, skip GAP
        pass
    
    x = BatchNormalization()(x)
    x = Dense(256, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(dropout_rate)(x)

    output = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=output)

    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False

    return model, base_model


def unfreeze_last_n_layers(base_model, n=30):
    """
    Unfreeze the LAST n layers of base_model.
    If n >= total, unfreezes all layers.
    Returns number of layers set trainable.
    """
    total = len(base_model.layers)
    start = max(0, total - n)

    for i, layer in enumerate(base_model.layers):
        layer.trainable = i >= start

    return sum(1 for l in base_model.layers if l.trainable)
