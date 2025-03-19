
import json
import time
from beta_tileManager import tile_manager

GAME_LOG_PATH = "game_log/my_simulate_gen_info.txt"
DELAY = 0.5  # 每条消息之间的延迟（秒）


def read_game_log():
    """ 逐条读取 `game_log.txt` 并调用 `tileManager` 处理 """
    prefix = "LiqiMsg: "

    with open(GAME_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("==================================================")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        if block.startswith(prefix):
            json_str = block[len(prefix):]  # 去掉前缀
        else:
            json_str = block

        try:
            liqi_msg = json.loads(json_str)

            if liqi_msg.get("state") == "GameStart":
                tile_manager.initialize_game(liqi_msg)
            elif liqi_msg.get("state") == "GameEnd":
                tile_manager.end_game()
            elif liqi_msg.get("name") == "ActionDiscardTile":
                tile_manager.handle_discard(liqi_msg["data"])

            time.sleep(DELAY)  # 模拟延迟，避免一次性写入过快

        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析错误: {e}")
        except Exception as e:
            print(f"⚠️ 处理 `LiqiMsg` 失败: {e}")


if __name__ == "__main__":
    read_game_log()  # 启动测试
