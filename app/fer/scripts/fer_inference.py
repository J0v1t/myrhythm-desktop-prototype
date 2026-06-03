import cv2
import os
import numpy as np
from pathlib import Path

from app.config.runtime_assets import DEFAULT_FER_MODEL, PROJECT_ROOT, resolve_runtime_assets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FER_DIR = os.path.join(BASE_DIR, "..")
MODEL_PATH = str(DEFAULT_FER_MODEL)


class FERModel:
     """
     Loads and runs predictions using the fine-tuned MyRhythm FER model.
     """

     def __init__(self, model_path=None, class_labels=None):
          # expected input size of model
          self.target_size = (48, 48)

          # default emotion classes 
          self.class_labels = (
               class_labels
               if class_labels
               else ["angry", "happy", "neutral", "sad"]
          )

          active_model_path = (
               Path(model_path)
               if model_path
               else resolve_runtime_assets().fer_model.path
          )
          if not active_model_path.is_absolute():
               active_model_path = PROJECT_ROOT / active_model_path
          active_model_path = active_model_path.resolve()

          if not active_model_path.exists():
               raise FileNotFoundError(f"FER model missing: {active_model_path}")

          from keras.models import load_model

          print("Loading model...")
          self.model = load_model(str(active_model_path))
          print("FER model loaded successfully.")

          # Haar cascade for face detection
          self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

     def preprocess_face(self, frame):
          """
          Detects a face, crops, resizes, and normalizes for model prediction.
          Returns (roi_gray, coords)
          """
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

          if len(faces) == 0:
               return None, None
          
          # Use the largest detected face (helps avoid false positives)
          x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]

          roi_gray = gray[y:y + h, x:x + w]
          roi_gray = cv2.resize(roi_gray, self.target_size)
          roi_gray = roi_gray.astype("float32") / 255.0
          roi_gray = np.expand_dims(roi_gray, axis=-1)  # add channel dimension

          return roi_gray, (x, y, w, h)
          
     def predict_emotion(self, frame):
          """
          Returns {'label': str, 'confidence': float} if face detected, else None.
          """
          roi, coords = self.preprocess_face(frame)
          if roi is None:
               return None

          roi = np.expand_dims(roi, axis=0)  # add batch dimension
          preds = self.model.predict(roi, verbose=0)[0]
          label = self.class_labels[np.argmax(preds)]
          confidence = float(np.max(preds))
          return {"label": label, "confidence": confidence, "coords": coords}

     def draw_prediction(self, frame, result):
          """
          Annotates frame with bounding box, label text, and semi-transparent background.
          Returns annotated frame.
          """
          x, y, w, h = result["coords"]
          label_text = f"{result['label']} ({result['confidence']*100:.1f}%)"

          # Border
          thickness = 2
          color = (255, 0, 0)  # Blue color
          cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

          # Font settings
          font = cv2.FONT_HERSHEY_SIMPLEX
          font_scale = 0.5
          thickness_text = 1
          text_color = (255, 255, 255)
          bg_color = (0, 0, 0)

          # Calculate text size
          (text_width, text_height), baseline = cv2.getTextSize(label_text, font, font_scale, thickness_text)

          # Position for text and background rectangle
          text_x = x
          text_y = y - 5 if y - 5 > text_height + 5 else y + h + text_height + 5

          # Rectangle coordinates for background
          rect_top_left = (text_x, text_y - text_height - baseline)
          rect_bottom_right = (text_x + text_width, text_y + baseline)

          # Ensure rectangle coordinates are within frame bounds
          height, width = frame.shape[:2]
          rect_top_left = (max(rect_top_left[0], 0), max(rect_top_left[1], 0))
          rect_bottom_right = (min(rect_bottom_right[0], width - 1), min(rect_bottom_right[1], height - 1))

          # Extract ROI
          roi = frame[rect_top_left[1]:rect_bottom_right[1], rect_top_left[0]:rect_bottom_right[0]]
          if roi.shape[0] > 0 and roi.shape[1] > 0:
              overlay = roi.copy()
              alpha = 0.7
              cv2.rectangle(overlay, (0, 0), (rect_bottom_right[0] - rect_top_left[0], rect_bottom_right[1] - rect_top_left[1]), bg_color, -1)
              cv2.addWeighted(overlay, alpha, roi, 1 - alpha, 0, roi)

          # Put the label text on the frame
          cv2.putText(frame, label_text, (text_x, text_y), font, font_scale, text_color, thickness_text, lineType=cv2.LINE_AA)

          return frame


if __name__ == "__main__":
    from camera_module import Camera

    cam = Camera()
    fer = FERModel()

    print("Running real-time FER test [press 'q' to quit]")

    while True:
        success, frame = cam.read_frame()
        if not success:
            break

        result = fer.predict_emotion(frame)
        if result:
            frame = fer.draw_prediction(frame, result)

        cv2.imshow("MyRhythm FER Test", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    print("Test finished.")
