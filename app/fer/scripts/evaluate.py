import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FER_DIR = os.path.join(BASE_DIR, "..")
TEST_DIR = os.path.join(FER_DIR, "fer_dataset", "test")
MODEL_PATH = os.path.join(FER_DIR, "trained_models/myrhythm_fer.h5")
LOG_PATH = os.path.join(FER_DIR, "artifacts/evaluation_log.json")

# Parameters
target_size = (48, 48)
batch_size = 64
class_labels = ['angry', 'happy', 'neutral', 'sad']  # adjust if needed

# Load model
model = load_model(MODEL_PATH)
print(f"Loaded model from {MODEL_PATH}")

# Test data generator
test_datagen = ImageDataGenerator(rescale=1./255)
test_gen = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=target_size,
    color_mode='grayscale',
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=False
)

# Evaluate model
loss, accuracy = model.evaluate(test_gen, verbose=1)
print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

# Predict labels
y_pred = model.predict(test_gen, verbose=1)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = test_gen.classes

# Report
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred_classes, target_names=class_labels, digits=4))

# Plot confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('FER Confusion Matrix (Test set)')
plt.tight_layout()
plt.show()

# Save evaluation log
eval_log = {
    'test_loss': float(loss),
    'test_accuracy': float(accuracy),
    'confusion_matrix': cm.tolist()
}

with open(LOG_PATH, 'w') as f:
    json.dump(eval_log, f)

print(f"Evaluation completed. Log saved at {LOG_PATH}")