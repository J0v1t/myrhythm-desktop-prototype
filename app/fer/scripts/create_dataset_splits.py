"""
Subject-safe dataset splitter for FER2013 + user images.
Ensures:
- FER2013 images are grouped into multiple pseudo-subjects.
- User images grouped by their subject prefix.
- aug images go ONLY to train.
- train/val/test contain all 4 emotions.

Output is written to fer_dataset/train|val|test/<emotion>/.
"""

import shutil
import random
from pathlib import Path
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
FER_DIR = BASE_DIR.parent                    # app/fer
PREPROCESSED_DIR = FER_DIR / "dataset_preprocessed"
ARTIFACTS_DIR = FER_DIR / "artifacts"
MANIFEST_PATH = ARTIFACTS_DIR / "dataset_manifest.csv"

OUTPUT_DIR = FER_DIR / "fer_dataset"
CLASS_NAMES = ["angry", "happy", "neutral", "sad"]

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-6
random.seed(42)

# -----------------------------
# SUBJECT EXTRACTION
# -----------------------------
def extract_subject(filename):
    """
    Assigns a subject ID based on filename.

    FER2013 images are numeric IDs → group them by buckets.
    Your own images must follow: subject_imageXX.jpg
    """
    name = filename.split(".")[0]

    # FER2013 → filename is digit-only
    if name.isdigit():
        # Make ~7 subjects (5000 images per subject)
        group = int(name) // 5000
        return f"fer2013_group_{group}"

    # User images → subject prefix before first underscore
    # example: jason_12.png → subject "jason"
    if "_" in name:
        return name.split("_")[0]

    # fallback
    return "unknown"


# -----------------------------
# COPY FILES HELPER
# -----------------------------
def copy_split(df_split, split_name):
    count = 0
    for _, row in df_split.iterrows():
        cls = row["label"]
        src = Path(row["preprocessed_path"])
        tgt = OUTPUT_DIR / split_name / cls / src.name
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, tgt)
        count += 1
    return count


# -----------------------------
# MAIN
# -----------------------------
def main():
    print("\n=== SUBJECT-SAFE SPLITTING STARTED ===\n")

    df = pd.read_csv(MANIFEST_PATH)

    # Assign subjects
    df["subject"] = df["preprocessed_path"].apply(
        lambda p: extract_subject(Path(p).name)
    )

    # Ensure source column exists
    if "source" not in df.columns:
        raise ValueError("ERROR: manifest missing 'source' column.")

    # Split augmented vs original
    df_aug = df[df["source"] == "augmented"]
    df_orig = df[df["source"] == "original"]

    subjects = list(df_orig["subject"].unique())
    random.shuffle(subjects)

    print(f"Total subjects detected: {len(subjects)}")
    print("Subjects:", subjects, "\n")

    n = len(subjects)
    n_train = int(n * TRAIN_RATIO)
    n_val = int(n * VAL_RATIO)

    train_subj = set(subjects[:n_train])
    val_subj = set(subjects[n_train:n_train + n_val])
    test_subj = set(subjects[n_train + n_val:])

    print("TRAIN subjects:", train_subj)
    print("VAL subjects:", val_subj)
    print("TEST subjects:", test_subj, "\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build splits
    df_train = df_orig[df_orig["subject"].isin(train_subj)]
    df_train = pd.concat([df_train, df_aug])  # aug only in train

    df_val = df_orig[df_orig["subject"].isin(val_subj)]
    df_test = df_orig[df_orig["subject"].isin(test_subj)]

    print("Sample counts:")
    print("  Train (original):", len(df_train) - len(df_aug))
    print("  Train (augmented):", len(df_aug))
    print("  Val:", len(df_val))
    print("  Test:", len(df_test))
    print()

    # Perform copy operations
    print("Copying train...")
    count_train = copy_split(df_train, "train")

    print("Copying val...")
    count_val = copy_split(df_val, "val")

    print("Copying test...")
    count_test = copy_split(df_test, "test")

    print("\n=== SUMMARY ===")
    print("Train images:", count_train)
    print("Val images:", count_val)
    print("Test images:", count_test)

    # Final sanity check: all emotions must appear in each split
    print("\nEmotion distribution check:")
    for split in ["train", "val", "test"]:
        for cls in CLASS_NAMES:
            path = OUTPUT_DIR / split / cls
            count = len(list(path.glob("*")))
            print(f"{split}/{cls}: {count}")
        print()

    print("=== SPLITTING COMPLETE ===\n")


if __name__ == "__main__":
    main()
