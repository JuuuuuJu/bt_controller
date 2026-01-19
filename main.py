import argparse
from bt_controller import ESP32BTSender
import time

PORT = 'COM3' 

def main():
    try:
        with ESP32BTSender(port=PORT) as sender:
            success = sender.send_burst(
                cmd_input='RESET',
                delay_sec=2, 
                prep_led_sec=1,
                target_ids=[0, 1, 5],
                data=[0, 0, 0],
                retries=3,
            )
            time.sleep(3)
            success = sender.send_burst(
                cmd_input='PLAY',
                delay_sec=3, 
                prep_led_sec=1,
                target_ids=[0, 1, 5],
                data=[0, 0, 0], # CANCEL: data[0]=cmd_id / TEST: rgb
                retries=3,
            )
            time.sleep(3)
            success = sender.send_burst(
                cmd_input='PAUSE',
                delay_sec=5, 
                prep_led_sec=1,
                target_ids=[0, 1, 5],
                data=[0, 0, 0],
                retries=3,
            )
            time.sleep(3)
            # success = sender.send_burst(
            #     cmd_input='CANCEL',
            #     delay_sec=1, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     data=[1, 0, 0],
            #     retries=3,
            # )
            # time.sleep(3)
            # success = sender.send_burst(
            #     cmd_input='TEST',
            #     delay_sec=7, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     data=[0, 0, 255],
            #     retries=3,
            # )
            # time.sleep(3)
            # success = sender.send_burst(
            #     cmd_input='RELEASE',
            #     delay_sec=9, 
            #     prep_led_sec=1,
            #     target_ids=[0, 1, 5],
            #     data=[0, 0, 0],
            #     retries=3,
            # )
            # time.sleep(3)
            
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()