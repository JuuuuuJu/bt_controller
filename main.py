import argparse
from bt_controller import ESP32BTSender
import time
PORT = 'COM3' 
def main():
    try:
        with ESP32BTSender(port=PORT) as sender:
            for i in range(100):
                success = sender.send_burst(
                    cmd_input='PLAY',
                    delay_sec=3, 
                    prep_led_sec=1,
                    target_ids=[0, 1, 5],
                    data=[0, 0, 0], # CANCEL: data[0]=cmd_id / TEST: rgb
                    retries=3,
                )
                if not success: print("PLAY failed")
    except Exception as e:
        print(f"Main execution error: {e}")
if __name__ == "__main__":
    main()