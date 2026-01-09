import argparse
from bt_controller import ESP32BTSender
import time

# 設定 Port (請修改為實際 Port)
PORT = 'COM13' 

def main():
    try:
        with ESP32BTSender(port=PORT) as sender:
            
            print("--- Test 1: Send PLAY Command ---")
            success = sender.send_burst(
                cmd_input='PLAY',
                delay_sec=1, 
                target_ids=[0, 1, 5],
                retries=3,
            )
            
            if success:
                print(">>> Test 1 Passed!")
            else:
                print(">>> Test 1 Failed!")
            
            time.sleep(2)

            print("--- Test 2: Send RESET Command ---")
            success = sender.send_burst(
                cmd_input='RESET',
                delay_sec=2, 
                target_ids=[0, 1, 5],
                retries=3,
            )
            
            if success:
                print(">>> Test 2 Passed!")
            else:
                print(">>> Test 2 Failed!")


    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()