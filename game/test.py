from game_state import GameState

# 创建 GameState 实例
game_state = GameState()

# liqi_msg 示例
liqi_msg = {
    'id': -1,
    'type': 'NOTIFY(1)',
    'method': '.lq.ActionPrototype',
    'data': {
        'step': 150,
        'name': 'ActionNoTile',
        'data': {
            'players': [
                {
                    'tingpai': True,
                    'hand': ['5m', '6m', '7m', '4p', '5p', '5p', '6p', '3s', '3s', '4s', '4s', '5s', '5s'],
                    'tings': [
                        {
                            'tile': '5p',
                            'haveyi': True,
                            'count': 3,
                            'fu': 40,
                            'countZimo': 4,
                            'fuZimo': 30,
                            'yiman': False,
                            'biaoDoraCount': 0,
                            'yimanZimo': False
                        }
                    ],
                    'alreadyHule': False
                },
                {
                    'tingpai': True,
                    'hand': ['1m', '1p', '2p', '3p', '1s', '2s', '3s', '7s', '8s', '9s'],
                    'tings': [
                        {
                            'tile': '1m',
                            'haveyi': True,
                            'count': 2,
                            'fu': 30,
                            'biaoDoraCount': 1,
                            'countZimo': 2,
                            'fuZimo': 30,
                            'yiman': False,
                            'yimanZimo': False
                        }
                    ],
                    'alreadyHule': False
                },
                {
                    'tingpai': True,
                    'hand': ['2p', '3p', '3z', '3z'],
                    'tings': [
                        {
                            'tile': '1p',
                            'fu': 30,
                            'fuZimo': 30,
                            'haveyi': False,
                            'yiman': False,
                            'count': 0,
                            'biaoDoraCount': 0,
                            'yimanZimo': False,
                            'countZimo': 0
                        },
                        {
                            'tile': '4p',
                            'fu': 30,
                            'fuZimo': 30,
                            'haveyi': False,
                            'yiman': False,
                            'count': 0,
                            'biaoDoraCount': 0,
                            'yimanZimo': False,
                            'countZimo': 0
                        }
                    ],
                    'alreadyHule': False
                },
                {
                    'tingpai': False,
                    'hand': [],
                    'tings': [],
                    'alreadyHule': False
                }
            ],
            'scores': [
                {
                    'oldScores': [26500, 18900, 49100, 4500],
                    'deltaScores': [1000, 1000, 1000, -3000],
                    'seat': 0,
                    'hand': [],
                    'ming': [],
                    'doras': [],
                    'score': 0,
                    'taxes': [],
                    'lines': []
                }
            ],
            'liujumanguan': False,
            'gameend': False,
            'hulesHistory': []
        }
    }
}

# 调用 input 方法
result = game_state.input(liqi_msg)

# 打印结果
print("Result:", result)
