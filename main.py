import argparse
from bt_controller import ESP32BTSender
import time

# 設定 Port (請修改為實際 Port)
PORT = 'COM13' 

def main():
    try:
        with ESP32BTSender(port=PORT) as sender:
            
            print("--- Test 1: Send Standard Command ---")
            success = sender.send_burst(
                cmd_type=0xA0, 
                burst_count=50, 
                delay_sec=1.0, 
                target_ids=[0, 1, 5],
                retries=3,
            )
            
            if success:
                print(">>> Test 1 Passed!")
            else:
                print(">>> Test 1 Failed!")


    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()