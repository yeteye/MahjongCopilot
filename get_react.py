import time
import json
import os
from bot_manager import BotManager
from common.settings import Settings
from game.game_state import GameState
from trans_to_cn import get_action_prompt

# 文件路径
GAME_LOG_PATH = "game_log/test.txt"
NEW_GAME_LOG_PATH = "game_log/new_game_log.txt"
REACTION_LOG_PATH = "game_log/reaction_log.txt"

# 监听状态
LAST_FILE_SIZE = 0  # 记录 `game_log.txt` 读取的位置
LAST_MODIFIED_TIME = 0  # 记录 `game_log.txt` 的修改时间

# 游戏结束信号
END_GAME_SIGNALS = ["ActionEndGame", "NotifyGameEndResult"]

# 全局变量保存 manager
_manager = None


def init_manager():
    """
    初始化全局 BotManager 实例，并启动线程。
    """
    global _manager
    if _manager is None:
        settings = Settings()
        _manager = BotManager(settings)
        _manager._create_bot()
        _manager.game_state = GameState(_manager.bot)
        _manager.start()
        time.sleep(0.2)  # 确保 AI 线程正常启动


def tail_file(file_path):
    """
    监听 `game_log.txt`，读取新追加的 `LiqiMsg`。
    """
    global LAST_FILE_SIZE, LAST_MODIFIED_TIME

    if not os.path.exists(file_path):
        return None  # 文件还未创建

    # 检查文件是否被修改
    modified_time = os.path.getmtime(file_path)
    if modified_time == LAST_MODIFIED_TIME:
        return None  # 文件未更新，不处理

    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(LAST_FILE_SIZE)  # 从上次读取的位置继续
        new_lines = f.readlines()
        LAST_FILE_SIZE = f.tell()  # 更新文件读取位置
        LAST_MODIFIED_TIME = modified_time  # 更新修改时间
        return new_lines


def process_new_liqi_msgs():
    """
    读取 `game_log.txt` 新增的 `LiqiMsg`，解析并处理，并同步到 `new_game_log.txt`。
    遇到游戏结束信号时，清空 `new_game_log.txt` 并继续监听新游戏。
    """
    init_manager()  # 确保 manager 已初始化

    while True:  # ✅ **持续监听 `game_log.txt`**
        new_lines = tail_file(GAME_LOG_PATH)

        if not new_lines:
            time.sleep(0.1)  # ✅ **短暂休眠，避免 CPU 过载**
            continue  # 没有新消息，继续监听

        prefix = "LiqiMsg: "
        for line in new_lines:
            line = line.strip()
            if line.startswith(prefix):
                json_str = line[len(prefix):]  # 去掉前缀
                try:
                    liqi_msg = json.loads(json_str, object_hook=liqi_object_hook)
                    method = liqi_msg.get("method", "")

                    # ✅ **将消息写入 `new_game_log.txt`**
                    with open(NEW_GAME_LOG_PATH, "a", encoding="utf-8") as new_log:
                        new_log.write(line + "\n")
                        new_log.write("=" * 50 + "\n")

                    # print(f"✅ 处理消息: {method}")

                    # 🚨 **检测游戏结束信号，清空 `new_game_log.txt`**
                    if any(end_signal in method for end_signal in END_GAME_SIGNALS):
                        print("🚨 检测到单局游戏结束信号，清空 `new_game_log.txt`")
                        with open(NEW_GAME_LOG_PATH, "w", encoding="utf-8") as new_log:
                            pass  # **清空文件**
                        continue  # **继续监听新的 `game_log.txt` 更新**

                    # 处理 reaction
                    reaction = _manager.my_api(liqi_msg)
                    if reaction:
                        prompt = get_action_prompt(reaction)  # 获取行动提示
                        print(f"行动提示: {prompt}")

                        # ✅ **将 reaction 记录到 `reaction_log.txt`**
                        with open(REACTION_LOG_PATH, "a", encoding="utf-8") as out_f:
                            out_f.write(json.dumps(reaction, ensure_ascii=False) + "\n")
                            out_f.write(f"行动提示: {prompt}\n")
                            out_f.write("=" * 50 + "\n")

                except json.JSONDecodeError as e:
                    print(f"❌ JSON 解析错误: {e}")


def react_api():
    """
    **持续监听 `game_log.txt`，当有新的 `liqi_msg` 进入时，进行处理并返回行动提示。**
    """
    print("📢 监听 `game_log.txt`，等待新 `LiqiMsg`...")
    process_new_liqi_msgs()  # **启动监听循环**


def liqi_object_hook(d):
    """
    解析 JSON 时，把 `type` 还原成 `MsgType`。
    """
    if "type" in d and isinstance(d["type"], str) and d["type"].startswith("MsgType."):
        enum_name = d["type"].split(".")[1]
        try:
            from liqi import MsgType
            d["type"] = MsgType[enum_name]
        except KeyError:
            pass
    return d


def add_liqi_msg_to_log(liqi_msg: dict):
    """
    ✅ **允许外部 API 调用，动态添加 `LiqiMsg` 到 `game_log.txt` 并触发 AI 处理。**
    """
    with open(GAME_LOG_PATH, "a", encoding="utf-8") as f:
        f.write("LiqiMsg: " + json.dumps(liqi_msg, ensure_ascii=False) + "\n")
        f.write("=" * 50 + "\n")

    # print(f"✅ 已添加新 `LiqiMsg`: {liqi_msg['method']}")
    time.sleep(0.1)  # **短暂等待，让监听器检测到变更**


if __name__ == "__main__":
    react_api()  # **启动监听**
