import json
from enum import Enum
from liqi import MsgType

#待优化

# 定义牌符号对应的中文名称字典
tile_mapping = {
        '1m': '一萬', '2m': '二萬', '3m': '三萬', '4m': '四萬', '5m': '伍萬',
        '6m': '六萬', '7m': '七萬', '8m': '八萬', '9m': '九萬',
        '1p': '一筒', '2p': '二筒', '3p': '三筒', '4p': '四筒', '5p': '伍筒',
        '6p': '六筒', '7p': '七筒', '8p': '八筒', '9p': '九筒',
        '1s': '一索', '2s': '二索', '3s': '三索', '4s': '四索', '5s': '伍索',
        '6s': '六索', '7s': '七索', '8s': '八索', '9s': '九索',
        'E': '東', 'S': '南', 'W': '西', 'N': '北',
        'C': '中', 'F': '發', 'P': '白',
        '5mr': '赤伍萬', '5pr': '赤伍筒', '5sr': '赤伍索',

}

action_mapping = {
        'reach': '立直', 'pon': '碰', 'kan_select':'杠',
        'chi_low': '吃-低', 'chi_mid': '吃-中', 'chi_high': '吃-高',
        'hora': '和牌', 'ryukyoku': '流局', 'none': '跳过', 'nukidora':'拔北'
}

def tile_to_chinese(tile_code: str) -> str:
    return tile_mapping.get(tile_code, tile_code)

def translate_reaction(reaction: dict):
    """
    将 reaction 信息转换成详细中文描述。
    """
    rtype = reaction.get("type")
    if rtype == "dahai":
        actor = reaction.get("actor")
        pai = reaction.get("pai")
        pai_cn = tile_to_chinese(pai)
        tsumogiri = reaction.get("tsumogiri")
        tsumo_text = "摸切" if tsumogiri else "非摸切"
        meta = reaction.get("meta", {})
        shanten = meta.get("shanten", "未知")
        eval_time = meta.get("eval_time_ns", "未知")
        greedy = meta.get("is_greedy", False)
        greedy_text = "采用贪心策略" if greedy else "未采用贪心策略"
        meta_options = reaction.get("meta_options", [])
        opts = []
        for op in meta_options:
            tile_option, prob = op
            tile_option_cn = tile_to_chinese(tile_option)
            opts.append(f"{tile_option_cn}(概率 {prob:.4f})")
        options_text = "；".join(opts)
        description = (f"【出牌】玩家 {actor} 打出牌 {pai_cn}，{tsumo_text}。"
                       f" 当前向听数为 {shanten}，模型评估耗时 {eval_time} 纳秒，{greedy_text}。"
                       f" 候选操作：{options_text}。")
        return description
    elif rtype == 'hora':
        return
    elif rtype == "none":
        meta = reaction.get("meta", {})
        shanten = meta.get("shanten", "未知")
        eval_time = meta.get("eval_time_ns", "未知")
        greedy = meta.get("is_greedy", False)
        greedy_text = "采用贪心策略" if greedy else "未采用贪心策略"
        meta_options = reaction.get("meta_options", [])
        opts = []
        for op in meta_options:
            tile_option, prob = op
            tile_option_cn = tile_to_chinese(tile_option)
            opts.append(f"{tile_option_cn}(概率 {prob:.4f})")
        options_text = "；".join(opts)
        description = (f"【无动作】当前向听数为 {shanten}，模型评估耗时 {eval_time} 纳秒，{greedy_text}。"
                       f" 候选操作：{options_text}。")
        return description
    else:
        return "未知的动作类型"

def get_action_prompt(reaction: dict) -> str:
    """
    仅提取 reaction 的关键信息，告诉用户建议的行动。
    如果 reaction 为出牌，则提示“建议玩家 X 出牌：Y（摸切/非摸切）”；
    如果为无动作，则提示“不采取行动”。
    """
    rtype = reaction.get("type")
    if rtype == "dahai":
        actor = reaction.get("actor")
        pai = reaction.get("pai")
        pai_cn = tile_to_chinese(pai)
        tsumogiri = reaction.get("tsumogiri")
        tsumo_text = "摸切" if tsumogiri else "非摸切"
        return f"建议玩家 {actor} 出牌：{pai_cn}（{tsumo_text}）。"
    elif rtype == "none":
        return "建议不采取行动。"
    else:
        return "无法识别建议的行动。"

def cn_api(reaction:str):
    reactions = json.loads(reaction)
    if reactions is None:
        return
    # description = translate_reaction(reactions)
    prompt = get_action_prompt(reactions)
    # print("详细描述：", description)
    print("行动提示：", prompt)
def main():
    reactions = []
    with open("new_reaction_log.txt", "r", encoding="utf-8") as f:
        reactions_json = f.read()
        blocks = reactions_json.split("==================================================")
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            try:
                reactions.append(block)
            except Exception as e:
                print("读取 block 时出错：", e)
    for js in reactions:
        try:
            reaction = json.loads(js)
            if reaction is None:
                continue
            description = translate_reaction(reaction)
            prompt = get_action_prompt(reaction)
            # print("详细描述：", description)
            print("行动提示：", prompt)
            print("-" * 50)
        except Exception as e:
            print("处理 reaction 时出错：", e)

if __name__ == "__main__":
    reaction = '{"type": "dahai", "actor": 1, "pai": "1s", "tsumogiri": true, "meta": {"q_values": [-9.254235, -8.504512, -6.8469095, -4.099716, -2.3322632, -8.218817, 0.094815016, -9.583127, -9.100557], "mask_bits": 51539885136, "is_greedy": true, "batch_size": 1, "eval_time_ns": 71805400, "shanten": 0, "at_furiten": false}, "meta_options": [["1s", 0.9049614589984416], ["4p", 0.07990305921214041], ["3p", 0.013644838797431244], ["2p", 0.0008747368681638228], ["5p", 0.00022185313724923256], ["7m", 0.00016672081033922202], ["5pr", 9.186091310538715e-05], ["5m", 7.877515214538084e-05], ["5mr", 5.669611098395818e-05]]}'
    cn_api(reaction)