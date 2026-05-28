import os
import json
import numpy as np
from pathlib import Path
from sklearn.utils import class_weight
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from model_utils import build_finetuned_fer_model, unfreeze_last_n_layers
from keras import backend as K

# Paths
BASE_DIR = Path(__file__).resolve().parent
FER_DIR = BASE_DIR.parent
DATA_DIR = FER_DIR / "fer_dataset"
MODEL_PATH = FER_DIR / "trained_models" / "myrhythm_fer.h5"
ARTIFACTS_DIR = FER_DIR / "artifacts" / "training_log.json"
LOG_PATH = FER_DIR / "artifacts"

IMG_SIZE = (48, 48)
BATCH_SIZE = 64

# Total epochs = WARMUP + FINE_TUNE
WARMUP_EPOCHS = 10
FINE_TUNE_EPOCHS = 20
TOTAL_EPOCHS = WARMUP_EPOCHS + FINE_TUNE_EPOCHS

# Fine-tuning params
UNFREEZE_LAST_N = 30          
FT_LEARNING_RATE = 1e-5       # low LR for fine-tuning

CLASS_NAMES = ["angry", "happy", "neutral", "sad"]

USE_FOCAL_LOSS = False   # set True to use focal loss (small datasets)

# ---------------------------
# Optional focal loss (Keras)
# ---------------------------
def focal_loss(gamma=2., alpha=0.25):
    def focal(y_true, y_pred):
        eps = 1e-7
        y_pred = K.clip(y_pred, eps, 1. - eps)
        cross_entropy = -y_true * K.log(y_pred)
        weight = alpha * K.pow(1 - y_pred, gamma)
        loss = weight * cross_entropy
        return K.sum(loss, axis=1)
    return focal

def main():
    # Generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.12,
        height_shift_range=0.12,
        shear_range=0.08,
        zoom_range=0.12,
        horizontal_flip=True,
        brightness_range=(0.7, 1.3),
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        DATA_DIR / "train",
        target_size=IMG_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    val_gen = val_datagen.flow_from_directory(
        DATA_DIR / "val",
        target_size=IMG_SIZE,
        color_mode='grayscale',
        class_mode='categorical',
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    # Compute class weights (Keras expects mapping from class index to weight)
    # train_gen.class_indices: e.g. {'angry':0,'happy':1,...}
    labels = train_gen.classes
    classes = np.unique(labels)
    cw = class_weight.compute_class_weight(class_weight='balanced', classes=classes, y=labels)
    class_weights = {int(cls): float(w) for cls, w in zip(classes, cw)}
    print("Class indices:", train_gen.class_indices)
    print("Computed class weights:", class_weights)

    # ----------------------------
    # Build model (warmup)
    # ----------------------------
    print("Building model (warmup, head only)...")
    model, base_model = build_finetuned_fer_model(num_classes=len(CLASS_NAMES))

    # Compile model
    if USE_FOCAL_LOSS:
        loss = focal_loss(gamma=2., alpha=0.25)
    else:
        loss = 'categorical_crossentropy'

    model.compile(optimizer=Adam(learning_rate=1e-3), loss=loss, metrics=['accuracy'])

    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss', 
            patience=8, 
            restore_best_weights=True,
            verbose=1
        ),

        ModelCheckpoint(
            str(MODEL_PATH),
            monitor='val_accuracy',
            verbose=1,
            save_best_only=True,
            mode='max'
        ),
        
        ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=4,
        min_lr=1e-6,
        verbose=1
        )
    ]

    # ----------------------------
    # Phase 1: Warmup (train head)
    # ----------------------------
    print(f"Phase 1: Warmup training for {WARMUP_EPOCHS} epochs (head only).")
    steps_per_epoch = max(1, train_gen.n // train_gen.batch_size)
    validation_steps = max(1, val_gen.n // val_gen.batch_size)

    history = model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        epochs=WARMUP_EPOCHS,
        validation_data=val_gen,
        validation_steps=validation_steps,
        class_weight=class_weights,
        callbacks=callbacks
    )

    # ----------------------------
    # Phase 2: Fine-tune (unfreeze top layers)
    # ----------------------------
    print("Phase 2: Unfreezing last", UNFREEZE_LAST_N, "layers of base model for fine-tuning.")
    num_unfrozen = unfreeze_last_n_layers(base_model, UNFREEZE_LAST_N)
    print("Unfrozen base model trainable layers:", num_unfrozen)

    # Recompile with a lower LR
    model.compile(optimizer=Adam(learning_rate=FT_LEARNING_RATE), loss='categorical_crossentropy', metrics=['accuracy'])

    print(f"Continue training for additional {FINE_TUNE_EPOCHS} epochs with LR={FT_LEARNING_RATE}")
    history = model.fit(
        train_gen,
        steps_per_epoch=steps_per_epoch,
        epochs=TOTAL_EPOCHS,
        initial_epoch=WARMUP_EPOCHS,
        validation_data=val_gen,
        validation_steps=validation_steps,
        class_weight=class_weights,
        callbacks=callbacks
    )

    print("Training finished. Best model (by val_accuracy) saved to:", MODEL_PATH)

    # Save training log
    os.makedirs(os.path.dirname(ARTIFACTS_DIR), exist_ok=True)

    # Convert numpy float32 to native floats in history.history for JSON serialization
    def convert_np_floats(obj):
        if isinstance(obj, dict):
            return {k: convert_np_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_np_floats(i) for i in obj]
        elif isinstance(obj, np.float32):
            return float(obj)
        else:
            return obj

    history_dict = convert_np_floats(history.history)

    with open(ARTIFACTS_DIR, 'w') as f:
        json.dump(history_dict, f)

    
if __name__ == "__main__":
    main()
