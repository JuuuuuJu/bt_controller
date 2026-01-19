import argparse
from bt_controller import ESP32BTSender
import time

# 設定 Port (請修改為實際 Port)
PORT = 'COM3' 

def main():
    try:
        with ESP32BTSender(port=PORT) as sender:
            # success = sender.send_burst(
            #     cmd_input='PLAY',
            #     delay_sec=4, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     r=0,
            #     g=0,
            #     b=0,
            #     retries=3,
            # )
            # time.sleep(3)
            
            # success = sender.send_burst(
            #     cmd_input='TEST',
            #     delay_sec=6, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     r=0,
            #     g=255,
            #     b=0,
            #     retries=3,
            # )
            # time.sleep(3)

            # success = sender.send_burst(
            #     cmd_input='RESET',
            #     delay_sec=7, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     r=0,
            #     g=0,
            #     b=0,
            #     retries=3,
            # )
            # time.sleep(3)
            success = sender.send_burst(
                cmd_input='LOAD',
                delay_sec=8, 
                prep_led_sec=1,
                target_ids=[0, 1, 5],
                r=0,
                g=0,
                b=0,
                retries=3,
            )
            time.sleep(3)
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()