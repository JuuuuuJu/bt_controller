import serial
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ESP32BTSender:
    CMD_MAP = { "RESET": 0x01, "READY": 0x02, "TEST": 0x03, "PLAY": 0xA0, "PAUSE": 0xA1 }

    def __init__(self, port, baud_rate=115200, timeout=1):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.ser.reset_input_buffer()
            logger.info(f"Connected to {self.port}")
        except serial.SerialException as e:
            logger.error(f"Failed to connect: {e}")
            raise

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_burst(self, cmd_input, delay_sec, prep_led_sec, target_ids, retries=3):
        if not self.ser or not self.ser.is_open:
            return False

        cmd_int = cmd_input if isinstance(cmd_input, int) else self.CMD_MAP.get(cmd_input, 0)
        delay_us = int(delay_sec * 1_000_000)
        prep_led_us = int(prep_led_sec * 1_000_000)
        target_mask = 0
        for pid in target_ids:
            target_mask |= (1 << pid)

        # 格式: 160,4000000,100000,23
        packet = f"{cmd_int},{delay_us},{prep_led_us},{target_mask:x}\n"

        for attempt in range(retries + 1):
            if attempt > 0:
                logger.warning(f"Retrying... ({attempt}/{retries})")
                time.sleep(0.1)

            logger.info(f"Sending: {packet.strip()}")
            
            try:
                self.ser.reset_input_buffer() # 發送前清空舊雜訊
                # [PC Start]
                t_start_pc = time.perf_counter()
                self.ser.write(packet.encode('utf-8'))

                # 等待 ACK (雖然沒有 Checksum，但確認收到還是必要的)
                start_time = time.time()
                while (time.time() - start_time) < (delay_sec + 2.0):
                    if self.ser.in_waiting:
                        line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                        
                        if "ACK:OK" in line:
                            # [PC End]
                            t_end_pc = time.perf_counter()
                            
                            # 1. 計算總 RTT (PC -> ESP -> PC)
                            total_rtt_us = (t_end_pc - t_start_pc) * 1_000_000
                            
                            # 2. 解析 ESP32 詳細計時
                            # 格式: ACK:OK:Read:Parse:Total
                            esp_read_us = 0.0
                            esp_parse_us = 0.0
                            esp_total_us = 0.0
                            
                            try:
                                parts = line.split(':')
                                # parts[0]="ACK", parts[1]="OK", parts[2]=Read, parts[3]=Parse, parts[4]=Total
                                if len(parts) >= 5:
                                    esp_read_us = float(parts[2])
                                    esp_parse_us = float(parts[3])
                                    esp_total_us = float(parts[4])
                            except ValueError:
                                logger.warning(f"Failed to parse timing: {line}")

                            # 3. 計算純傳輸延遲 (USB + Driver + Cable)
                            transport_us = total_rtt_us - esp_total_us
                            
                            print("\n" + "="*40)
                            print(f"Latency Analysis (Attempt {attempt+1})")
                            print("="*40)
                            print(f"Total Round-Trip Time : {total_rtt_us:8.2f} us")
                            print(f"  ├─ Transport (USB/OS) : {transport_us:8.2f} us")
                            print(f"  └─ ESP32 Internal     : {esp_total_us:8.2f} us")
                            print(f"       ├─ RingBuf Read  : {esp_read_us:8.2f} us")
                            print(f"       └─ Logic & Parse : {esp_parse_us:8.2f} us")
                            print("="*40 + "\n")
                            
                            return True
                        elif "NAK" in line:
                            logger.warning(f"Device rejected command: {line}")
                            break 
            except Exception as e:
                logger.error(f"Error: {e}")

        logger.error("Failed to send command after retries.")
        return False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()