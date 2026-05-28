import numpy as np

class KalmanFilterHR:
    """
    Implements a simple 1D Kalman Filter to track a heart rate state
    and filter out noise/measurement errors from the raw broadcast BPM.
    
    This is critical for stabilizing the noisy smartwatch HR data.
    """
    def __init__(self, initial_bpm=80, process_variance=0.1, measurement_variance=2.0, initial_error=1.0):
        """
        Initializes the Kalman Filter parameters.

        Args:
            initial_bpm (float): The starting estimate for the heart rate state.
            process_variance (float): Q - How much the true HR can change between steps (trust of the model).
            measurement_variance (float): R - How much noise is in the observation (trust of the measurement).
            initial_error (float): P - Initial confidence in the state estimate.
        """
        # State: The true Heart Rate (HR) estimate
        self.state = initial_bpm
        
        # P: Estimate error covariance (how confident we are in the state estimate)
        self.P = initial_error
        
        # Q: Process Noise (Process Variance) - Higher Q trusts the measurement more.
        self.Q = process_variance
        
        # R: Measurement Noise (Measurement Variance) - Higher R trusts the prediction more.
        self.R = measurement_variance
        
    def filter(self, measurement_bpm: float) -> float:
        """
        Performs the two steps of the Kalman Filter: Prediction and Update.
        
        Args:
            measurement_bpm (float): The raw HR value broadcast by the sensor.
            
        Returns:
            float: The filtered (corrected) HR value.
        """
        
        # --- 1. Prediction Step ---
        # Predict the next state (assuming constant velocity, A=1, B=0)
        # We assume the HR doesn't change much from one measurement to the next.
        self.state = self.state 
        
        # Predict the next error covariance
        self.P = self.P + self.Q
        
        # --- 2. Update Step ---
        # Calculate the Kalman Gain (K)
        # K determines how much the measurement should influence the prediction.
        K = self.P / (self.P + self.R)
        
        # Update the state estimate
        self.state = self.state + K * (measurement_bpm - self.state)
        
        # Update the error covariance
        self.P = (1 - K) * self.P
        
        return self.state

    def get_current_estimate(self) -> float:
        """Returns the current filtered state estimate."""
        return self.state