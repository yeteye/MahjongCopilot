import time
import json
import os
import threading
from bot_manager import BotManager
from common.settings import Settings
from game.game_state import GameState
from trans_to_cn import get_action_prompt
from prompt_ui import update_ui

GAME_LOG_PATH = "game_log/test.txt"
REACTION_LOG_PATH = "game_log/reaction_log.txt"

LAST_FILE_SIZE = 0  # 记录 `game_log.txt` 读取的位置
LAST_MODIFIED_TIME = 0  # 记录 `game_log.txt` 的修改时间

END_GAME_SIGNALS = ["ActionEndGame", "NotifyGameEndResult"]

_manager = None


def init_manager():
    global _manager
    if _manager is None:
        settings = Settings()
        _manager = BotManager(settings)
        _manager._create_bot()
        _manager.game_state = GameState(_manager.bot)
        _manager.start()
        time.sleep(0.4)  # 确保 AI 线程正常启动


def tail_file(file_path):
    global LAST_FILE_SIZE, LAST_MODIFIED_TIME

    if not os.path.exists(file_path):
        return None  # **文件未创建，跳过**

    # **检查文件是否更新**
    modified_time = os.path.getmtime(file_path)
    if modified_time == LAST_MODIFIED_TIME:
        return None  # **文件无变更，跳过**

    with open(file_path, "r", encoding="utf-8") as f:
        f.seek(LAST_FILE_SIZE)  # **从上次读取的位置继续**
        new_lines = f.readlines()
        LAST_FILE_SIZE = f.tell()  # **更新文件指针**
        LAST_MODIFIED_TIME = modified_time  # **更新修改时间**
        return new_lines


def process_new_liqi_msgs():

    init_manager()  # **确保 AI 启动**

    while True:
        new_lines = tail_file(GAME_LOG_PATH)

        if not new_lines:
            time.sleep(0.1)  # **避免 CPU 过载**
            continue

        prefix = "LiqiMsg: "
        for line in new_lines:
            line = line.strip()
            if line.startswith(prefix):
                json_str = line[len(prefix):]  # **去掉前缀**
                try:
                    liqi_msg = json.loads(json_str, object_hook=liqi_object_hook)
                    method = liqi_msg.get("method", "")

                    if any(end_signal in method for end_signal in END_GAME_SIGNALS):
                        print("游戏结束，清空 `game_log.txt`")
                        with open(GAME_LOG_PATH, "w", encoding="utf-8") as new_log:
                            new_log.truncate(0)  # **清空文件**
                        continue

                    # print("now processing: ",liqi_msg)
                    reaction = _manager.my_api(liqi_msg)
                    # print("right")
                    if reaction:
                        prompt = get_action_prompt(reaction)  # **获取行动提示**
                        print(f"行动提示: {prompt}")

                        update_ui(prompt)  # **实时更新 UI**

                        with open(REACTION_LOG_PATH, "a", encoding="utf-8") as out_f:
                            out_f.write(json.dumps(reaction, ensure_ascii=False) + "\n")
                            out_f.write(f"行动提示: {prompt}\n")
                            out_f.write("=" * 50 + "\n")

                except json.JSONDecodeError as e:
                    print(f"JSON 解析错误: {e}")


def react_api():
    print("监听 `game_log.txt`，等待新 `LiqiMsg`...")
    process_new_liqi_msgs()


def liqi_object_hook(d):
    if "type" in d and isinstance(d["type"], str) and d["type"].startswith("MsgType."):
        enum_name = d["type"].split(".")[1]
        try:
            from liqi import MsgType
            d["type"] = MsgType[enum_name]
        except KeyError:
            pass
    return d


def add_liqi_msg_to_log(liqi_msg: dict):

    with open(GAME_LOG_PATH, "a", encoding="utf-8") as f:
        f.write("LiqiMsg: " + json.dumps(liqi_msg, ensure_ascii=False) + "\n")
        f.write("=" * 50 + "\n")

    time.sleep(0.1)  # **短暂等待，让监听器检测到变更**


