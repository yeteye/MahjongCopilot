import time
import json
import threading

from get_react import add_liqi_msg_to_log,react_api  # ✅ **导入 `add_liqi_msg_to_log`**

WHOLE_GAME_LOG_PATH = "game_log/my_simulate_gen_info.txt"  # **完整游戏日志**
DELAY_BETWEEN_MESSAGES = 0.05  # **每条消息之间的延迟（秒）**


def read_whole_game_log():
    """
    读取 `whole_game_log.txt`，逐条解析 `LiqiMsg` 并调用 `add_liqi_msg_to_log()` 进行输入。
    """
    prefix = "LiqiMsg: "
    with open(WHOLE_GAME_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("==================================================")  # **按分隔符拆分**

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        if block.startswith(prefix):
            json_str = block[len(prefix):]  # **去掉前缀**
        else:
            json_str = block

        try:
            liqi_msg = json.loads(json_str)  # **解析 JSON**
            # print(f"📤 发送消息到 `game_log.txt`: {liqi_msg['method']}")
            add_liqi_msg_to_log(liqi_msg)  # **调用 API 添加到 `game_log.txt`**

            time.sleep(DELAY_BETWEEN_MESSAGES)  # **模拟延迟，避免一次性写入过快**

        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}")
        except Exception as e:
            print(f"⚠️ 处理 `LiqiMsg` 失败: {e}")




if __name__ == "__main__":
    # **启动 react_api 线程**
    react_thread = threading.Thread(target=react_api, daemon=True)
    react_thread.start()

    # **继续执行 read_whole_game_log**
    read_whole_game_log()
