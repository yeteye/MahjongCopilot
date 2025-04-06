import time
import json
import threading
import os
from prompt_ui import PromptUI
from get_react import add_liqi_msg_to_log, react_api
# from medium import mid_func
from beta_generator import convert_image_data

WHOLE_GAME_LOG_PATH = "game_log/my_simulate_gen_info.txt"
PRE_PATH = "game_log/pre.txt"
DELAY_BETWEEN_MESSAGES = 0.05  # 处理每条消息的时间间隔
POLL_INTERVAL = 0.1  # 轮询新数据的间隔（单位：秒）

last_file_size = 0  # 记录上次读取的文件大小
last_file_size_2 = 0 


def tail_game_log():

    global last_file_size  # **使用全局变量**
    global last_file_size_2

    while True:
        # print("iscalled")
        if not os.path.exists(WHOLE_GAME_LOG_PATH):
            time.sleep(1)
            continue  # **等待文件创建后再处理**
        if not os.path.exists(PRE_PATH):
            time.sleep(1)
            continue  # **等待文件创建后再处理**

        # **检查文件大小，判断是否有新内容**
        current_size_1 = os.path.getsize(WHOLE_GAME_LOG_PATH)
        current_size_2 = os.path.getsize(PRE_PATH)

        if current_size_1 > last_file_size:  # **文件变大，说明有新内容**
            print(f"发现新数据: 旧大小 {last_file_size} → 新大小 {current_size_1}")

            # **读取新增的内容**
            with open(WHOLE_GAME_LOG_PATH, "r", encoding="utf-8") as f:
                f.seek(last_file_size)  # **从上次读取的位置继续**
                new_lines = f.readlines()
                last_file_size = f.tell()  # **更新全局 `last_file_size`**

            # **解析新增的 `LiqiMsg` 并处理**
            process_new_liqi_msgs(new_lines,0)
        
        if current_size_2 > last_file_size_2:  # **文件变大，说明有新内容**
            print(f"发现新数据: 旧大小 {last_file_size_2} → 新大小 {current_size_2}")

            # **读取新增的内容**
            with open(PRE_PATH, "r", encoding="utf-8") as f:
                f.seek(last_file_size_2)  # **从上次读取的位置继续**
                new_lines = f.readlines()
                last_file_size_2 = f.tell()  # **更新全局 `last_file_size`**

            # **解析新增的 `LiqiMsg` 并处理**
            process_new_liqi_msgs(new_lines,1)


        time.sleep(POLL_INTERVAL)  # **短暂休眠，避免 CPU 过载**


def process_new_liqi_msgs(new_lines,flag):
    if flag == 0:
        prefix = "LiqiMsg: "
        for line in new_lines:
            line = line.strip()
            if line.startswith(prefix):
                json_str = line[len(prefix):]  # **去掉前缀**
            else:
                json_str = line

            try:
                # print("处理消息: ", json_str)
                liqi_msg = json.loads(json_str)  # **解析 JSON**
                add_liqi_msg_to_log(liqi_msg)  # **调用 API 添加到 `game_log.txt`**
                time.sleep(DELAY_BETWEEN_MESSAGES)  # **模拟延迟**

            except json.JSONDecodeError:
                continue
            except Exception as e:
                continue
    else:
        for line in new_lines:
            line = line.strip()
            json_str = line

            try:
                print("处理消息: ", json_str)
                raw_msg = json.loads(json_str)  # **解析 JSON**
                liqi_msg_2=convert_image_data(raw_msg)
                if isinstance(liqi_msg_2, list):
                    for liqi_msg in liqi_msg_2:
                        with open(WHOLE_GAME_LOG_PATH, "a", encoding="utf-8") as f:
                            f.write("LiqiMsg: " + json.dumps(liqi_msg, ensure_ascii=False) + "\n")
                            f.write("=" * 50 + "\n")
                else:  # 如果只返回一个字典
                    with open(WHOLE_GAME_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write("LiqiMsg: " + json.dumps(liqi_msg_2, ensure_ascii=False) + "\n")
                        f.write("=" * 50 + "\n")


                time.sleep(DELAY_BETWEEN_MESSAGES)  # **模拟延迟**

            except json.JSONDecodeError:
                continue
            except Exception as e:
                continue

    return


def main():
    # print("iscalled")
    # pre_thread = threading.Thread(target=mid_func, daemon=True)
    # pre_thread.start()

    react_thread = threading.Thread(target=react_api, daemon=True)
    react_thread.start()

    log_thread = threading.Thread(target=tail_game_log, daemon=True)
    log_thread.start()

    while True:
        time.sleep(0.3)


if __name__ == "__main__":
    main()
