import asyncio
import os
import sys
import time

# --- IMPORT FIX ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
# --- END IMPORT FIX ---

try:
    from app.hr.scripts.ble_reader import read_heart_rate_live
    # Import the new function from pipeline
    from app.hr.scripts.pipeline import predict_emotions_live, get_current_filtered_bpm, calculate_final_emotion_and_save 
    from app.hr.trained_hr_models.hr_feature_engineering import SEQUENCE_LENGTH
    from app.hr.trained_hr_models.classifier import load_model_components
except ImportError as e:
    print(f"❌ Error during import: {e}")
    print("Ensure all required Python files are present and using correct imports.")
    sys.exit(1)

# Global configuration
stop_event = asyncio.Event()
SHUTDOWN_DURATION_SECONDS = 40 # Automatically stop after 40 seconds

def hr_data_handler(raw_bpm: int):
    """
    Callback function that runs the prediction pipeline on every new HR reading.
    """
    # 1. Feed the raw BPM into the prediction pipeline and unpack both labels
    predicted_quadrant, real_emotion = predict_emotions_live(raw_bpm)
    
    # 2. Get the filtered BPM estimate
    filtered_bpm = get_current_filtered_bpm()

    # --- Output Formatting (MODIFIED TO USER REQUEST) ---
    display_emotion = real_emotion

    if predicted_quadrant == "Buffering Data":
        display_emotion = "N/A"
        
    status_message = (
        f"Raw BPM: {raw_bpm:3d} | Filtered BPM: {filtered_bpm:6.2f} | "
        f"Quadrant: {predicted_quadrant:11s} | Real Emotion: {display_emotion:<10s}"
    )
    
    # Overwrite the previous line for a dynamic display
    # Print the status message, followed by spaces to clear any remnants of a longer previous line.
    print(f"\r{status_message}" + " " * 40, end='', flush=True)

async def shutdown_timer(duration: int):
    """Stops the application after a specified duration."""
    print(f"\nMonitoring will automatically stop in {duration} seconds...")
    await asyncio.sleep(duration)
    
    # --- FIX: Clear the dynamic status line before printing static shutdown message ---
    sys.stdout.write('\r' + ' ' * 100 + '\r') 
    sys.stdout.flush()
    
    # Set the event to stop the main BLE task
    stop_event.set()
    print("⏰ Time limit reached. Stopping monitoring...")


async def main():
    """The main asynchronous entry point for the real-time monitor."""
    print("--- Real-Time Emotion Monitoring System ---")
    print(f"Model and Encoder loading... ", end='')
    if load_model_components():
        print("✅ Success.")
        print(f"Prediction sequence length required: {SEQUENCE_LENGTH} seconds.")
    else:
        print("❌ FAILED. Ensure model files are present.")
        return

    try:
        print("\nStarting BLE monitoring...")
        
        # Start the timer task and the BLE reading task concurrently
        timer_task = asyncio.create_task(shutdown_timer(SHUTDOWN_DURATION_SECONDS))
        ble_task = asyncio.create_task(read_heart_rate_live(hr_data_handler, stop_event))

        # Wait for both tasks to finish (i.e., when stop_event is set by the timer or Ctrl+C)
        await asyncio.gather(timer_task, ble_task)
        
    except KeyboardInterrupt:
        # --- FIX: Clear the dynamic status line before printing final message ---
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.flush()
        print("\nKeyboard interrupt detected. Stopping...")
    finally:
        # Ensure the stop event is set to clean up any lingering tasks
        stop_event.set()
        
        # --- FIX: Clear the dynamic status line before printing final message ---
        sys.stdout.write('\r' + ' ' * 100 + '\r')
        sys.stdout.flush()
        
        # Calculate and save the final emotion upon shutdown
        print("💾 Calculating and saving final emotion...")
        calculate_final_emotion_and_save()
        
        print("\nApplication gracefully shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Ctrl+C] Main process interruption caught.")
    except RuntimeError as e:
        if "cannot run more than one event loop" in str(e):
             print("\n❌ Event loop already running. The main function can only be run once.")
        else:
            raise