import asyncio
from typing import Callable, Optional
import sys

# Standard BLE UUIDs
HR_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
HR_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

# Common keywords in HR device names to help detection if UUID is missing from advertisement
HR_DEVICE_NAMES = ["polar", "hrm", "wahoo", "garmin", "coospo", "heart"]

_client: Optional[object] = None


def _load_bleak():
    from bleak import BleakScanner, BleakClient, BleakError

    return BleakScanner, BleakClient, BleakError

# ----------------------------------------------------------
# BLE Utilities
# ----------------------------------------------------------

def _is_hr_device(device, advertisement_data):
    """
    Heuristic to determine if a device is likely a Heart Rate Monitor.
    Checks Service UUIDs first, then falls back to Device Name.
    """
    # 1. Check for the Heart Rate Service UUID in the advertisement data
    if HR_SERVICE_UUID.lower() in [u.lower() for u in advertisement_data.service_uuids]:
        return True
    
    # 2. Fallback: Check if the device name indicates it is an HR monitor
    # (Useful for devices that don't advertise the UUID to save bits)
    if device.name:
        if any(keyword in device.name.lower() for keyword in HR_DEVICE_NAMES):
            return True
            
    return False

async def find_hr_device() -> Optional[object]:
    """Scans for BLE devices and returns the first valid HR device found."""
    try:
        BleakScanner, _, _ = _load_bleak()
    except ImportError as e:
        print(f"BLE support unavailable: {e}")
        return None

    print("🔍 Scanning for BLE devices (5s)...")
    
    # We scan for ALL devices (no filter) because some HR monitors
    # don't broadcast their service UUIDs in the advertisement packet.
    devices_dict = await BleakScanner.discover(timeout=5.0, return_adv=True)

    found_hr_devices = []

    for device, adv_data in devices_dict.values():
        if _is_hr_device(device, adv_data):
            found_hr_devices.append(device)
            print(f"   ✅ Found candidate: {device.name} ({device.address})")

    if not found_hr_devices:
        print("❌ No specific Heart Rate devices identified.")
        print("   (Ensure device is on and not connected to another app/phone)")
        return None

    # Sort by RSSI (Signal Strength) to pick the closest one
    # Note: 'rssi' attribute availability depends on OS, usually in adv_data or device details
    target_device = found_hr_devices[0]
    print(f"🎯 Selecting strongest/first device: {target_device.name} - {target_device.address}")
    return target_device


def parse_hr_measurement(data: bytearray) -> Optional[int]:
    """Parses the Heart Rate Measurement characteristic data."""
    if not data:
        return None
        
    flags = data[0]
    hr_format = flags & 0x01  # Bit 0: 0=uint8, 1=uint16

    if hr_format == 0:  # 8-bit
        return data[1] if len(data) > 1 else None
    else:  # 16-bit
        if len(data) > 2:
            return (data[2] << 8) | data[1]
        return None


_parse_hr_measurement = parse_hr_measurement


async def read_heart_rate_live(
    bpm_callback: Callable[[int], None],
    stop_event: asyncio.Event,
) -> bool:
    global _client

    try:
        _, BleakClient, BleakError = _load_bleak()
    except ImportError as e:
        print(f"BLE support unavailable: {e}")
        return False
    
    # 1. Find the device
    device = await find_hr_device()
    if not device:
        return False

    def hr_notification_handler(sender: int, data: bytearray):
        bpm = parse_hr_measurement(data)
        if bpm is not None:
            bpm_callback(bpm)

    # 2. Connection Loop with Retry
    # We try connecting up to 3 times because BLE connections often fail on the first try
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"⏳ Waiting for adapter to settle (Attempt {attempt+1}/{max_retries})...")
            # CRITICAL: Pause between scan and connect to let the OS bluetooth stack reset
            await asyncio.sleep(2.0) 

            print(f"🔗 Connecting to {device.address}...")
            async with BleakClient(device.address, timeout=15.0) as client:
                _client = client
                
                if not client.is_connected:
                    print("❌ Connection failed (is_connected=False).")
                    continue

                print(f"✅ Connected to {device.name}!")
                
                # Check if the device actually has the HR service before subscribing
                # (This handles the case where we matched by Name but it's not actually an HR monitor)
                services = client.services
                if not services.get_service(HR_SERVICE_UUID):
                    print("❌ Device connected, but Heart Rate Service (0x180d) not found.")
                    return False

                print("📡 Starting heart rate notifications...")
                await client.start_notify(HR_CHAR_UUID, hr_notification_handler)

                # Keep the connection alive until stop_event is set
                while not stop_event.is_set():
                    if not client.is_connected:
                        print("⚠️ Connection lost unexpectedly.")
                        break
                    await asyncio.sleep(1.0)

                print("🛑 Stopping notifications...")
                await client.stop_notify(HR_CHAR_UUID)
                return True

        except BleakError as e:
            print(f"⚠️ BLE Error on attempt {attempt+1}: {e}")
            _client = None
        except asyncio.CancelledError:
            print("🛑 Task cancelled.")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            _client = None

    print("❌ Failed to connect after multiple attempts.")
    return False

def stop_streaming_if_running():
    """Reserved for external thread interruption."""
    # Since we use context managers, this is mostly a placeholder or for forceful disconnects.
    pass

# ------------------------------------------------------------------
# Entry Point (for testing this script directly)
# ------------------------------------------------------------------
if __name__ == "__main__":
    async def main():
        stop_ev = asyncio.Event()
        
        def print_bpm(bpm):
            print(f"❤️  BPM: {bpm}")

        # Run for 20 seconds then stop
        task = asyncio.create_task(read_heart_rate_live(print_bpm, stop_ev))
        await asyncio.sleep(20)
        stop_ev.set()
        await task

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
