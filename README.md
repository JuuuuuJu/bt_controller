# ESP32 BLE Sender - UART Controlled

本專案提供了一個封裝好的 Python 模組 bt_controller.py。這個模組實現了一個透過 PC 端 Python 腳本經由 UART (USB Serial) 控制 ESP32 發送藍牙 (BLE) 廣播指令封包的系統。

1. 安裝需求

pip install -r requirements.txt

2. API 說明

# Class: ESP32BTSender

__init__(port, baud_rate=115200, timeout=1):

# port: (必填) 序列埠名稱。
# baud_rate: 預設為 115200 (需與 ESP32 設定一致)。

send_burst(cmd_type, burst_count, delay_sec, target_ids):

# cmd_type (int): 指令代碼 (e.g., 0xA0).
# burst_count (int): 連續發送次數.
# delay_sec (float): 預期送達時間 (秒).
# target_ids (list): 目標設備 ID 列表 (e.g., [0, 2, 5]).
# Return: True 代表執行成功且收到 ESP32 回應；False 代表失敗或超時.

3. 使用範例

from bt_controller import ESP32BTSender

# 請修改為實際 COM Port
PORT = 'COM13' 

with ESP32BTSender(port=PORT) as sender:
    # 發送指令：類型 0xA0，發 50 次，倒數 3 秒，給 player ID 0 和 1
    if sender.send_burst(0xA0, 50, 3.0, [0, 1]):
        print("Passed")
    else:
        print("Failed")