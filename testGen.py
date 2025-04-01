from beta_generator import convert_image_data
import json

image_data_list2 = [
    {"state": "GameStart", "seatList": [101, 17457800, 102, 103],
     "tiles": ["8p", "5m", "7s", "9m", "7s", "4m", "7m", "0m", "4z", "2p", "3p", "7m", "4p"],
     "doras": ["7m"],
    "chang": 0},

    {"state": "Discard", "seat": 0, "tile": "E"},
    {"state": "MyAction", "getTile": "7m", "tile": "4z"},
    {"state": "Discard",  "seat": 2, "tile": "9s"},
    {"state": "Discard",  "seat": 3, "tile": "N"},

    {"state": "Discard",  "seat": 0, "tile": "E"},
    {"state": "MyAction",  "getTile": "7s", "tile": "9m"},
    {"state": "Discard",  "seat": 2, "tile": "3p"},
    {"state": "Discard",  "seat": 3, "tile": "W"},

    {"state": "Discard",  "seat": 0, "tile": "4m"},
    {"state": "MyAction",  "getTile": "3m", "tile": "8p"},
    {"state": "Discard",  "seat": 2, "tile": "6s"},
    {"state": "Discard",  "seat": 3, "tile": "B"},

    {"state": "Discard", "seat": 0, "tile": "5m"},
    {"state": "MyAction",  "getTile": "4p", "tile": "4p"},
    {"state": "Discard", "seat": 2, "tile": "7p"},
    {"state": "Discard",  "seat": 3, "tile": "F"},

    {"state": "Discard",  "seat": 0, "tile": "6m"},
    {"state": "MyAction",  "getTile": "1m", "tile": "1m"},
    {"state": "Discard",  "seat": 2, "tile": "8p"},
    {"state": "Discard",  "seat": 3, "tile": "C"},

    {"state": "Discard",  "seat": 0, "tile": "7m"},
    {"state": "MyAction_Chipongang", "doras": ["7m"], "tile": "2p", "operation": {
        "type": 3,
        "combination": ["7m", "7m", "7m"],
    }},
    {"state": "Discard",  "seat": 2, "tile": "9p"},
    {"state": "Discard",  "seat": 3, "tile": "1s"},

    {"state": "Discard",  "seat": 0, "tile": "8m"},
    {"state": "MyAction",  "getTile": "1m", "tile": "5m"},
    {
        "state":"Other_Chipongang",
        "seat":3,
        "tile": "3s",
        "doras":["7m"],
        "operation":{
            "type": 3,
            "combination":["5m","5m","5m"],
        }
    },

    {"state": "Discard",  "seat": 0, "tile": "2m"},
    {"state": "MyAction_Chipongang","doras": ["7m"], "tile":"7s" ,"operation": {
        "type": 2,
        "combination": ["2m", "3m", "4m"],
    }},
     {"state": "GameEnd"}
    ]

with open("game_log/my_simulate_gen_info.txt", "w", encoding="utf-8") as f:
    for image_data in image_data_list2:
        liqi_msgs = convert_image_data(image_data)
        for msg in liqi_msgs:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
            f.write(f"LiqiMsg: {json.dumps(msg, ensure_ascii=False)}\n")
            f.write("==================================================\n")