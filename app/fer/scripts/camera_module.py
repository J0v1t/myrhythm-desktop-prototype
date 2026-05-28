import cv2

class Camera:
    """
    Handles webcam capture and frame retrieval.
    """

    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        self.available = True
        if not self.cap.isOpened():
            self.available = False
        
        # set frame size only if camera available
        if self.available:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read_frame(self):
        """
        Capture one frame from webcam.
        Returns (success, frame)
        """
        if not self.available or not self.cap:
            return False, None
        return self.cap.read()
    
    def release(self):
        """
        Release camera safely.
        """
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()


# --- Run this file directly to test webcam feed ---   
if __name__ == "__main__":
    cam = Camera()
    if not cam.available:
        print("Camera not accessible. Exiting.")
    else:
        print("Press 'q' to quit.")

        while True:
            success, frame = cam.read_frame()
            if not success:
                print("Frame not captured.")
                break

            cv2.imshow("Mood Detection Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cam.release()
        print("Camera released.")
