import os
import time
import json
from beta_generator import convert_image_data

# 输入文件（监听）
INPUT_FILE = "gamelog/pre.txt"

# 输出文件（写入转换后的内容）
OUTPUT_FILE = "game_log/my_simulate_gen_info.txt"

POLL_INTERVAL = 0.3  # 轮询间隔（秒）

# 记录上次读取的位置
last_file_size = 0

def process_new_lines(lines):
    """解析 A.txt 的新增行，并转换后写入 B.txt"""
    converted_msgs = []  # 用于存储转换后的 JSON 数据

    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        try:
            json_data = json.loads(line)  # 解析 A.txt 的 JSON
            converted_data = convert_image_data(json_data)  # 调用转换函数
            print("isCalled")
            # 确保 convert_image_data 返回的是列表（可能是多个消息）
            if not isinstance(converted_data, list):
                converted_data = [converted_data]

            for msg in converted_data:
                converted_msgs.append(json.dumps(msg, ensure_ascii=False))  # 转换成 JSON 字符串

        except json.JSONDecodeError:
            print("JSON 解析失败:", line)

    # 追加写入 B.txt
    if converted_msgs:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            for msg in converted_msgs:
                f.write(f"{msg}\n")  # 逐行写入
            f.write("==================================================\n")  # 分隔符

def mid_func():
    while True:
        print("isCalled1")
        if not os.path.exists(INPUT_FILE):
            time.sleep(1)
            continue  # **等待 A.txt 创建后再处理**

        # **检查文件大小，判断是否有新内容**
        current_size = os.path.getsize(INPUT_FILE)

        if current_size > last_file_size:  # **文件变大，说明有新内容**
            print(f"发现新数据: 旧大小 {last_file_size} → 新大小 {current_size}")

            # **读取新增的内容**
            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                f.seek(last_file_size)  # **从上次读取的位置继续**
                new_lines = f.readlines()
                last_file_size = f.tell()  # **更新 `last_file_size`**

            # **解析新增 JSON 并转换后写入 B.txt**
            process_new_lines(new_lines)

        time.sleep(POLL_INTERVAL)  # **短暂休眠，避免 CPU 过载**

