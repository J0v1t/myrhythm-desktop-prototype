import os
import cv2
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "datasets", "fer", "fer2013.csv"))
OUTPUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "dataset"))

emotion_map = {
    0: "angry",
    3: "happy",
    4: "sad",
    6: "neutral"
}

df = pd.read_csv(CSV_PATH)
print("CSV loaded successfully.")

df = df[df['emotion'].isin(emotion_map.keys())]
print(f"Filtered dataset size: {len(df)} samples")

os.makedirs(OUTPUT_DIR, exist_ok=True)

for label in emotion_map.values():
    os.makedirs(os.path.join(OUTPUT_DIR, label), exist_ok=True)

count = 0

for idx, row in df.iterrows():
    emotion = row['emotion']
    pixels = list(map(int, row['pixels'].split()))

    # Reshape into 48x48 grayscale
    img = np.array(pixels, dtype='uint8').reshape((48, 48))

    # Output path
    folder = emotion_map[emotion]
    img_path = os.path.join(OUTPUT_DIR, folder, f"{idx}.png")

    # Save image
    cv2.imwrite(img_path, img)
    count += 1

print(f"Done! Saved {count} images into `{OUTPUT_DIR}/`.")
