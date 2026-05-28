import cv2
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FER_DIR = os.path.join(BASE_DIR, "..")

DATASET_DIR = os.path.join(FER_DIR, "dataset")
AUGMENTED_DIR = os.path.join(DATASET_DIR, "augmented")
PREPROCESSED_DIR = os.path.join(FER_DIR, "dataset_preprocessed")
ARTIFACTS_DIR = os.path.join(FER_DIR, "artifacts")

EMOTIONS = ["angry", "happy", "neutral", "sad"]

os.makedirs(PREPROCESSED_DIR, exist_ok=True)
for emotion in EMOTIONS:
    os.makedirs(os.path.join(PREPROCESSED_DIR, emotion), exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

print("Running preprocessing...")

os.makedirs(ARTIFACTS_DIR, exist_ok=True)
MANIFEST_PATH = os.path.join(ARTIFACTS_DIR, "dataset_manifest.csv")

def process_folder(folder_path, emotion, source_type, writer):
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            print("Skipping unreadable:", img_path)
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face = gray[y:y+h, x:x+w]
        else:
            face = gray

        face_resized = cv2.resize(face, (48, 48))
        save_path = os.path.join(PREPROCESSED_DIR, emotion, img_name)
        cv2.imwrite(save_path, face_resized)

        writer.writerow([img_path, save_path, emotion, source_type])

with open(MANIFEST_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["original_path", "preprocessed_path", "label", "source"])

    # ORIGINAL IMAGES
    for emotion in EMOTIONS:
        folder = os.path.join(DATASET_DIR, emotion)
        process_folder(folder, emotion, "original", writer)
        
    # AUGMENTED IMAGES
    if os.path.exists(AUGMENTED_DIR):
        for emotion in ["angry", "sad"]:
            folder = os.path.join(AUGMENTED_DIR, emotion)
            process_folder(folder, emotion, "augmented", writer)

print("Preprocessing complete. Manifest saved at:", MANIFEST_PATH)
