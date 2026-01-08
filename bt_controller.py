import serial
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ESP32BTSender:
    def __init__(self, port, baud_rate=115200, timeout=1):
        """
        Initialize ESP32 BT Sender
        :param port: Serial Port (e.g., 'COM13')
        :param baud_rate: Baud Rate (Default: 115200)
        :param timeout: Serial Read Timeout
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)
            self.ser.write(b'\n')
            time.sleep(0.1)
            self.ser.reset_input_buffer()
            logger.info(f"Connected to {self.port}")
        except serial.SerialException as e:
            logger.error(f"Failed to connect to {self.port}: {e}")
            raise

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Serial connection closed.")

    def send_burst(self, cmd_type, burst_count, delay_sec, target_ids, retries=3):
        """
        Send burst command to ESP32 BT device
        :param cmd_type: 指令類型 (int, e.g., 0xA0)
        :param burst_count: 發送次數 (int)
        :param delay_sec: 總延遲時間 (秒)
        :param target_ids: 目標 ID 列表 (list of int, e.g., [0, 1])
        :return: (bool) True if success, False otherwise
        """
        if not self.ser or not self.ser.is_open:
            logger.error("Serial port not open. Call connect() first.")
            return False

        delay_us = int(delay_sec * 1_000_000)
        target_mask = 0
        for pid in target_ids:
            target_mask |= (1 << pid)

        command_str = f"{cmd_type},{burst_count},{delay_us},{target_mask:x}\n"
        
        for attempt in range(retries + 1):
            if attempt > 0:
                logger.warning(f"Retrying command (Attempt {attempt}/{retries})...")

            logger.info(f"Sending Command: {command_str.strip()}")
            
            try:
                self.ser.reset_input_buffer()
                self.ser.write(command_str.encode('utf-8'))
                start_time = time.time()
                wait_timeout = delay_sec + 2.0
                
                while (time.time() - start_time) < wait_timeout:
                    if self.ser.in_waiting:
                        line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                        
                        if "RESULT:OK" in line:
                            logger.info(f"Command executed successfully. Device response: {line}")
                            return True
                        elif "RESULT:ERROR" in line:
                            logger.warning(f"Device reported format error: {line}")
                            break 
                
                if attempt == retries:
                    logger.error("Timeout or Error waiting for device response.")

            except Exception as e:
                logger.error(f"Error during communication: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()