from beta_generator import convert_image_data

import json

image_data_list2 = [
    # ---------- 开局阶段 ----------
    {"state": "GameStart", "seatList": [101, 17457800, 102, 103],
     "tiles": ["8p", "5m", "7s", "9m", "7s", "5s", "7m", "0m", "4z", "2p", "3p", "7m", "4p"],
     "doras": ["7m"],  # 初始宝牌指示牌
    "chang": 0}, # 场

    # ---------- 第一巡 ----------
    {"state": "Discard", "seat": 0, "tile": "E"},  # 玩家0弃东风
    {"state": "MyAction", "getTile": "7m", "tile": "4z"},  # 玩家3(我方)弃1万
    {"state": "Discard",  "seat": 2, "tile": "9s"},  # 玩家1弃9索
    {"state": "Discard",  "seat": 3, "tile": "N"},   # 玩家2弃北风


    # ---------- 第二巡（碰牌触发）----------
    {"state": "Discard",  "seat": 0, "tile": "E"},   # 玩家0再弃东风
    {"state": "MyAction",  "getTile": "7s", "tile": "9m"},
    {"state": "Discard",  "seat": 2, "tile": "3p"},  # 玩家1弃3筒（宝牌）
    {"state": "Discard",  "seat": 3, "tile": "W"},   # 玩家2弃西风
               # 我方弃2万

    # ---------- 第三巡（吃牌触发）----------
    {"state": "Discard",  "seat": 0, "tile": "4m"},  # 玩家0弃4万
    {"state": "MyAction",  "getTile": "3m", "tile": "8p"},
    {"state": "Discard",  "seat": 2, "tile": "6s"}, # 玩家1弃6索
    {"state": "Discard",  "seat": 3, "tile": "B"},  # 玩家2弃白板
     # 我方弃3万

    # ---------- 第四巡（杠牌触发）----------
    {"state": "Discard", "seat": 0, "tile": "5m"},
    {"state": "MyAction",  "getTile": "4p", "tile": "4p"},
    {"state": "Discard", "seat": 2, "tile": "7p"},
    {"state": "Discard",  "seat": 3, "tile": "F"},  # 玩家2弃发
              # 我方弃4筒

    # ---------- 第五巡（连续鸣牌）----------
    {"state": "Discard",  "seat": 0, "tile": "6m"},
    {"state": "MyAction",  "getTile": "1m", "tile": "1m"},
    {"state": "Discard",  "seat": 2, "tile": "8p"},
    {"state": "Discard",  "seat": 3, "tile": "C"},  # 玩家2弃中
     # 我方弃5筒

    # ---------- 第六巡（宝牌变更）----------
    {"state": "Discard",  "seat": 0, "tile": "7m"},
    {"state": "MyAction",  "getTile": "3p", "tile": "2p"},
    {"state": "Discard",  "seat": 2, "tile": "9p"},
    {"state": "Discard",  "seat": 3, "tile": "1s"},
    # 我方弃6筒

    # ---------- 第七巡（流局阶段）----------
    {"state": "Discard",  "seat": 0, "tile": "8m"},
    {"state": "MyAction",  "getTile": "5m", "tile": "5m"},
    {"state": "Discard",  "seat": 2, "tile": "2s"},
    {"state": "Discard",  "seat": 3, "tile": "3s"},
     # 我方弃7索

    # ---------- 第八巡（最后回合）----------
    {"state": "Discard",  "seat": 0, "tile": "9m"},
    {"state": "MyAction",  "getTile": "5m", "tile": "5m"},
    {"state": "Discard",  "seat": 2, "tile": "4s"},
    {"state": "Discard",  "seat": 3,  "tile": "3s"},
    {"state": "GameEnd"}  # 流局结束
]
# 处理所有数据
with open("game_log/my_simulate_gen_info.txt", "w", encoding="utf-8") as f:
    for image_data in image_data_list2:
        liqi_msgs = convert_image_data(image_data)
        # 遍历每个消息单独写入
        for msg in liqi_msgs:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
            # 添加前缀并转换为单行JSON
            f.write(f"LiqiMsg: {json.dumps(msg, ensure_ascii=False)}\n")
            # 添加分隔线
            f.write("==================================================\n")