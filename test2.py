import json, time
from bot_manager import BotManager
from common.settings import Settings
from game.game_state import GameState
from bot import Bot, get_bot


def simulated_message_source():
    """
    模拟一个消息生成器，从文件或列表中逐条返回 liqi_msg。
    这里假设你已将手动输入的 liqi_msg 保存在一个列表中。
    """
    messages = []
    with open("simulate.txt", "r", encoding="utf-8") as f:
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
                msg = json.loads(json_str)
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
        except Exception as e:
            print(f"liqi_msg: {liqi_msg}")
            print("Error processing liqi_msg:", e)
            times += 1
            reaction = 'Error'
        with open("reaction_log.txt", "w", encoding="utf-8") as outfile:
            if reaction is not None:
                print(reaction)
                # 写入输出文件，每个 reaction 之间用分隔符分隔
                outfile.write(json.dumps(reaction, ensure_ascii=False) + "\n")
                outfile.write("==================================================\n")

    # 停止线程
    manager.stop(join_thread=True)


if __name__ == "__main__":
    main()
