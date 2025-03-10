import json
from bot_manager import BotManager
from common.settings import Settings  # 假设 Settings 类存在
from game.game_state import GameState
from bot import Bot, get_bot


def main():
    # 初始化 Settings 和 BotManager（真实环境下会加载真实 Bot 引擎）
    settings = Settings()  # 根据需要初始化 Settings 的各个属性
    manager = BotManager(settings)

    # 生成 Bot 实例并创建 GameState
    manager.bot = None
    manager._create_bot()

    print(manager.bot)

    manager.game_state = GameState(manager.bot)

    # 输入和输出文件名
    input_filename = "whole_game_log.txt"
    output_filename = "reaction_log.txt"

    reactions = []  # 用于存放所有返回的 reaction
    with open(input_filename, "r", encoding="utf-8") as infile, \
            open(output_filename, "w", encoding="utf-8") as outfile:
        # 读取整个文件内容，然后按照分隔符划分，每个块包含一条 liqi_msg 的 JSON 字符串
        content = infile.read()
        # 假设分隔符为 "=================================================="
        blocks = content.split("==================================================")
        for block in blocks:
            # 保留 JSON 字符串内部的空格，不对其内容进行删除操作
            block = block.rstrip()  # 仅去除右侧多余空白
            if not block:
                continue
            prefix = "Liqi_msg: "
            idx = block.find(prefix)
            if idx == -1:
                continue
            # 提取 prefix 后面的 JSON 部分
            json_str = block[idx + len(prefix):]
            try:
                liqi_msg = json.loads(json_str)
            except json.JSONDecodeError as e:
                print("JSON 解析错误:", e)
                continue


            # 调用 my_api 并捕获异常，确保错误不影响后续处理
            try:
                reaction = manager.my_api(liqi_msg)
            except Exception as e:
                print("Error processing liqi_msg:", e)
                reaction = 'Error'

            # 如果 reaction 不为空，将其保存
            if reaction is not None:
                reactions.append(reaction)
                # 写入输出文件，每个 reaction 之间用分隔符分隔
                outfile.write(json.dumps(reaction, ensure_ascii=False) + "\n")
                outfile.write("==================================================\n")

    # 打印所有 reaction
    print("所有 reaction 处理完成：")
    for r in reactions:
        print(r)



if __name__ == "__main__":
    main()
