import json, time
from bot_manager import BotManager
from common.settings import Settings
from game.game_state import GameState
from bot import Bot, get_bot
import json
from enum import Enum
from liqi import MsgType
from trans_to_cn import get_action_prompt,cn_api

def liqi_object_hook(d):
    # 如果字典中有 "type" 字段，且它是形如 "MsgType.REQ" 的字符串
    if "type" in d and isinstance(d["type"], str):
        if d["type"].startswith("MsgType."):
            enum_name = d["type"].split(".")[1]
            try:
                d["type"] = MsgType[enum_name]
            except KeyError:
                # 如果转换失败，保持原样
                pass
    return d

def unique_hook(d):
    return d

def simulated_message_source():
    """
    模拟一个消息生成器，从文件或列表中逐条返回 liqi_msg。
    这里假设你已将手动输入的 liqi_msg 保存在一个列表中。
    """
    messages = []
    with open("game_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
        blocks = content.split("==================================================")
        prefix = "LiqiMsg: "
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            if block.startswith(prefix):
                json_str = block[len(prefix):]
            else:
                json_str = block
            try:
                # 使用自定义 object_hook 进行解码
                msg = json.loads(json_str, object_hook=liqi_object_hook)

                messages.append(msg)
            except Exception as e:
                print("解析错误:", e)
    for m in messages:
        yield m
        time.sleep(0.05)  # 模拟延时


def main():
    settings = Settings()  # 根据实际情况初始化
    manager = BotManager(settings)
    # 创建 Bot 并 GameState
    manager._create_bot()
    manager.game_state = GameState(manager.bot)

    # 启动 BotManager 的线程
    manager.start()

    times=0
    # 模拟将消息注入到 mitm_server 消息队列中
    # 一种方法：你可以修改 mitm_server.get_message() 让它从你的生成器中取消息
    # 或者在这里直接调用 _process_msg 模拟处理
    for liqi_msg in simulated_message_source():
        # 模拟直接处理消息（你也可以构造一个 Dummy WSMessage 对象）
        # print("Injecting message:", liqi_msg)

        # 直接调用 my_api 模拟处理：注意这不会更新所有内部状态，
        # 如果希望走完整的流程，建议模拟 WSMessage 然后调用 _process_msg

        try:
            reaction = manager.my_api(liqi_msg)

            str_reaction = json.dumps(reaction)
            cn_api(str_reaction)


            # print("my reaction", reaction)
            # with open("new_reaction_log.txt", "a", encoding="utf-8") as outfile:
            #     outfile.write(json.dumps(reaction, ensure_ascii=False) + "\n")
            #     outfile.write("==================================================\n")
        except Exception as e:
            print(f"liqi_msg: {liqi_msg}")
            print("Error processing liqi_msg:", e)
            times += 1
            reaction = 'Error'

    # 停止线程
    manager.stop(join_thread=True)

def react_api():
    main()


if __name__ == "__main__":
    main()
