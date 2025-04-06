import json

def init():
    #清空my_simulate_gen_info.txt和pre.txt
    with open('game_log/my_simulate_gen_info.txt', 'w') as f:
        pass
    with open('game_log/pre.txt', 'w') as f:
        pass
    with open('game_log/test.txt', 'w') as f:
        pass