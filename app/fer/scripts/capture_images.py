import numpy as np
import cv2
import os
import csv

# --- User input ---
subject_id = input("Enter subject ID (e.g., jason, user01): ").strip().lower()
if subject_id == "":
    print("ERROR: Subject ID cannot be empty.")
    exit()

# Base dataset path
script_dir = os.path.dirname(__file__)
dataset_path = os.path.join(script_dir, '..', 'dataset')

# Emotion folders
emotions = ["happy", "sad", "angry", "neutral"]
for emotion in emotions:
    os.makedirs(os.path.join(dataset_path, emotion), exist_ok=True)

# Augmented data folders
aug_root = os.path.join(dataset_path, "augmented")
os.makedirs(aug_root, exist_ok=True)
for emotion in ["sad", "angry"]:  # only target minority classes
    os.makedirs(os.path.join(aug_root, emotion), exist_ok=True)

# CSV metadata logging
csv_path = os.path.join(dataset_path, "captured_metadata.csv")
csv_exists = os.path.isfile(csv_path)

csv_file = open(csv_path, 'a', newline='')
csv_writer = csv.writer(csv_file)

if not csv_exists:
    csv_writer.writerow(["filename", "subject", "emotion", "type"])  
    # type: raw or augmented

# Webcam initialization
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("\n=== Capture Controls ===")
print("h = happy | s = sad | a = angry | n = neutral")
print("SPACE = capture | q = quit")
print("========================\n")

current_emotion = None

# --- Augmentation function ---
def augment_image(img):
    """Return a list of augmented versions of the image."""
    aug_images = []

    # Small rotation
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), 15, 1)
    aug_images.append(cv2.warpAffine(img, M, (w, h)))

    # Horizontal flip
    aug_images.append(cv2.flip(img, 1))

    # Brightness shift
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.add(hsv[:, :, 2], 30)
    aug_images.append(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR))

    return aug_images

# --- Capture loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "No frame detected", (50, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    display_text = f"Emotion: {current_emotion if current_emotion else 'None'} | Subject: {subject_id}"
    cv2.putText(frame, display_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):
        break

    # Change emotion label
    if key == ord('h'): current_emotion = "happy"
    elif key == ord('s'): current_emotion = "sad"
    elif key == ord('a'): current_emotion = "angry"
    elif key == ord('n'): current_emotion = "neutral"

    # Capture frame
    elif key == 32:  # SPACE
        if current_emotion is None:
            print("Choose emotion first (h/s/a/n)")
            continue

        # Save raw image
        emotion_folder = os.path.join(dataset_path, current_emotion)
        subject_files = [f for f in os.listdir(emotion_folder) if f.startswith(subject_id + "_")]
        img_num = len(subject_files) + 1

        filename = f"{subject_id}_{current_emotion}_{img_num:03d}.jpg"
        img_path = os.path.join(emotion_folder, filename)
        cv2.imwrite(img_path, frame)

        csv_writer.writerow([filename, subject_id, current_emotion, "raw"])
        print(f"Saved RAW: {img_path}")

        # Apply targeted augmentation
        if current_emotion in ["sad", "angry"]:
            aug_images = augment_image(frame)
            aug_folder = os.path.join(aug_root, current_emotion)

            for i, aug_img in enumerate(aug_images, 1):
                aug_filename = f"{subject_id}_{current_emotion}_{img_num:03d}_aug{i}.jpg"
                aug_path = os.path.join(aug_folder, aug_filename)
                cv2.imwrite(aug_path, aug_img)

                csv_writer.writerow([aug_filename, subject_id, current_emotion, "augmented"])
                print(f"Saved AUG: {aug_path}")

csv_file.close()
cap.release()
cv2.destroyAllWindows()
