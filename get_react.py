import json, time
from bot_manager import BotManager
from common.settings import Settings
from game.game_state import GameState
from bot import Bot, get_bot
from trans_to_cn import get_action_prompt  # 此函数返回一个中文提示字符串

# 全局变量保存 manager
_manager = None


def init_manager():
    """
    初始化全局 BotManager 实例，并启动线程。
    这个实例会保持状态，用于后续逐条处理 liqi_msg。
    """
    global _manager
    if _manager is None:
        settings = Settings()  # 根据实际情况初始化 Settings
        _manager = BotManager(settings)
        _manager._create_bot()
        _manager.game_state = GameState(_manager.bot)
        _manager.start()
        # 适当等待，确保内部状态初始化完成
        time.sleep(0.2)


def react_api(liqi_msg: dict) -> str:
    """
    接收一条 liqi_msg（字典格式），处理后返回中文的行动提示字符串。
    该函数会使用全局的 BotManager 实例，保持内部状态连续更新。
    """
    global _manager
    if _manager is None:
        init_manager()
    try:
        reaction = _manager.my_api(liqi_msg)
        # 如果 reaction 为空，返回一个提示
        if reaction is None:
            return "当前无有效反应。"
        # 使用 get_action_prompt 获取简短行动提示
        prompt = get_action_prompt(reaction)
        return prompt
    except Exception as e:
        return f"处理 liqi_msg 出错: {e}"


# 以下为一个测试示例，仅供参考
if __name__ == "__main__":
    # 模拟一条 liqi_msg（这里直接用一个例子）
    sample_str = '{"id": 1, "type": "MsgType.RES", "method": ".lq.FastTest.authGame", "data": {"players": [{"accountId": 17457800, "avatarId": 400101, "nickname": "猫机", "level": {"id": 10101, "score": 18}, "character": {"charid": 200001, "exp": 200, "skin": 400101, "level": 0, "views": [], "isUpgraded": false, "extraEmoji": [], "rewardedLevel": []}, "level3": {"id": 20101, "score": 0}, "title": 0, "avatarFrame": 0, "verified": 0, "views": []}], "seatList": [13, 17457800, 11, 12], "gameConfig": {"category": 1, "mode": {"mode": 3, "ai": true, "detailRule": {/*...*/}, "extendinfo": ""}, "meta": {"roomId": 10143, "modeId": 0, "contestUid": 0}}, "readyIdList": [13, 11, 12], "isGameStart": false}}'


    # 为保证类型一致性，可以使用 object_hook 转换 "type" 字段
    def liqi_object_hook(d):
        if "type" in d and isinstance(d["type"], str) and d["type"].startswith("MsgType."):
            enum_name = d["type"].split(".")[1]
            try:
                from liqi import MsgType
                d["type"] = MsgType[enum_name]
            except KeyError:
                pass
        return d


    liqi_msg = json.loads(sample_str, object_hook=liqi_object_hook)

    # 调用 react_api 处理单条消息，并打印提示
    prompt = react_api(liqi_msg)
    print("行动提示：", prompt)
