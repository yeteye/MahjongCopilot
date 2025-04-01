import json
import random


class TileManager:
    def __init__(self, player_id):
        self.player_id = player_id  # 我方玩家 ID
        self.Myseat = 0           # 我方座位号
        self.hands = []             # 我方手牌
        self.doras = []             # 宝牌指示牌

        self.myDoras = []

        self.melds = {i: [] for i in range(4)}  # 各玩家的明牌（吃/碰/杠）
        self.discards = {i: [] for i in range(4)}  # 各玩家的弃牌
        self.seat_map = {}          # 玩家 ID 到座位号的映射
        self.cancel_chipongang = []

        self.can_chipongang = False  # 存储待处理的吃/碰/杠操作

        self.lastPlayer = 0
        self.currentPlayer = 0

        self.lastTile = "1m"
        self.currentTile = "1m"

        self.forbiden = []
        self.is_liqi = False          # 我方是否立直
        self.justLiqi = False       # 是否刚刚立直
        self.can_liqi = False

        self.zhenting = False         # 我方是否振听
        self.tingpai = []             # 我方听牌列表
        self.liqiTodeal = []  # 立直后的限定出牌
        self.lastChi = []

        # 新增属性
        self.current_operationList = []  # 当前可操作牌列表（例如吃碰杠的组合）
        self.step = 0                    # 当前步骤，方便消息 step 自增
        self.player = {}                 # 存储每个座位的玩家信息，包括立直等
        self.scores = [25000, 25000, 25000, 25000]  # 各玩家得分
        self.liqibang = 0                # 全局立直棒数量
        self.leftTileCount = 69          # 剩余牌数
        self.liqiScore = 24000           # 立直时对应分数

    def initialize_game(self, data):
        """ 初始化游戏状态 """
        # 构造座位映射：seat -> playerId
        self.seat_map = {seat: player for seat, player in enumerate(data["seatList"])}
        self.cancel_chipongang = []
        # 设置我方座位号
        self.Myseat = next(seat for seat, player in self.seat_map.items() if player == self.player_id)
        self.hands = data["tiles"]
        self.doras = data["doras"]
        self.melds = {i: [] for i in range(4)}
        self.discards = {i: [] for i in range(4)}

        self.lastPlayer = 0
        self.currentPlayer = 0

        self.lastTile = "1m"
        self.currentTile = data.get("tile", "1m")

        self.lastChi = []
        self.forbiden = []
        self.can_chipongang = False
        self.justLiqi = False

        self.liqiTodeal = []      #立直后的限定出牌
        self.zhenting = False  # 我方是否振听
        self.tingpai = []  # 我方听牌列表

        self.current_operationList = []
        self.step = 0
        self.liqibang = 0  # 每局开始重置立直棒数量
        # 初始化每个玩家的默认状态（扩展字段：听牌、是否立直、振听等）
        for seat, player in self.seat_map.items():

            self.player[seat] = {
                "accountId": player,
                "tingpai": [],
                "is_liqi": False,
                "liqi": False,
                "zhenting": False
            }

        print("游戏初始化完成")

    def is_furiten(self):
        """
        参数：
          waiting_tiles: list[str]，己方当前可能和牌的候选牌（听牌列表）
          self_discards: list[str]，己方已经弃掉的牌列表
        说明：
          根据日本麻将规则，如果玩家自己弃过自己待听（赢牌）的牌，则视为振听。
          此函数简单判断听牌列表中是否有任一牌已经被弃出。
        """
        waiting_tiles = [entry["tile"] for entry in self.tingpai]

        self_discards = self.discards[self.Myseat]

        for tile in waiting_tiles:
            if tile in self_discards:
                self.zhenting = True
                break
            else:
                self.zhenting = False

        return

    def is_hupai(self, hand):
        """
        判断 14 张牌的 hand 是否和牌（日本麻将和牌判断的简化示例）
        采用一般形：4个面子 + 1雀头；同时也考虑 7对子形式。
        这里只处理数字牌，不处理字牌和特殊役，作为示例。
        """
        if len(hand) != 14:
            return False

        # 7对子判断：如果 hand 中有7个不同牌且每个牌至少出现2次
        counts = {}
        for tile in hand:
            counts[tile] = counts.get(tile, 0) + 1
        if len([tile for tile, cnt in counts.items() if cnt >= 2]) == 7:
            return True

        # 尝试从 hand 中选出一对雀头，然后递归判断剩下是否能拆分成4个面子（三张一组，刻子或顺子）
        for tile in counts:
            if counts[tile] >= 2:
                counts[tile] -= 2
                if self._can_form_melds(counts):
                    counts[tile] += 2
                    return True
                counts[tile] += 2
        return False

    def _can_form_melds(self, counts):
        """ 递归判断 counts 中的牌能否拆分成面子（刻子或顺子） """
        # 如果所有牌都拆分完，则和牌成立
        if all(cnt == 0 for cnt in counts.values()):
            return True
        # 找到第一个还有牌的 tile
        for tile in sorted(counts.keys()):
            if counts[tile] > 0:
                break
            # 尝试刻子
            if counts[tile] >= 3:
                counts[tile] -= 3
                if self._can_form_melds(counts):
                    return True
                counts[tile] += 3
            # 尝试顺子（仅适用于数字牌）
            if len(tile) == 2 and tile[0].isdigit():
                num = int(tile[0])
                suit = tile[1]
                tile2 = f"{num + 1}{suit}"
                tile3 = f"{num + 2}{suit}"
                if tile2 in counts and tile3 in counts and counts[tile2] > 0 and counts[tile3] > 0:
                    counts[tile] -= 1
                    counts[tile2] -= 1
                    counts[tile3] -= 1
                    if self._can_form_melds(counts):
                        return True
                    counts[tile] += 1
                    counts[tile2] += 1
                    counts[tile3] += 1
        return False

    def tileCount(self, tile):
        total = 0
        for i in range(4):
            total += self.melds[i].count(tile)
            total += self.discards[i].count(tile)
        total += self.hands.count(tile)
        return total
    def count_tingpaiList(self):

        self.tingpai = []  # 重新初始化听牌列表
        hand_copy = self.hands.copy()
        # for meld in self.melds[self.Myseat]:
        #     hand_copy.remove(meld)

        for i in hand_copy:
              # 复制手牌
            hand_copy_2 = self.hands.copy()
            hand_copy_2.remove(i)  # 在副本上移除 i

            waiting = self.compute_tingpai(hand_copy_2)  # 传入副本
            if waiting:
                self.tingpai.append({
                    "tile": i,
                    "zhenting": self.zhentingif(i),
                    "infos": [{
                        "tile": j,
                        "haveyi": True,
                        "count": 4-self.tileCount(j),
                        "fu": 30,
                        "biaoDoraCount": len(self.doras),
                        "countZimo": 2,
                        "fuZimo": 20,
                        "yiman": False,
                        "yimanZimo": False
                    } for j in waiting]  # 这里填充所有可能的听牌信息
                })
        return
    def zhentingif(self,tile):
        if self.zhenting:
            return True
        else:
            if tile in self.discards[self.Myseat]:
                return True
        return False

    def compute_tingpai(self,hand):
        waiting = []
        candidate_tiles = []
        # 这里只处理数字牌；扩展时可加入风牌和箭牌
        for suit in ["m", "p", "s"]:
            for num in range(1, 10):
                candidate_tiles.append(f"{num}{suit}")

        # 假设当前 hand 为 self.hands 中少一张（己方已出一张），或者另外保存待摸牌的 13 张
        current_hand = hand.copy()

        if len(current_hand) != 13:
            # 为示例，若手牌不为 13 张则返回空
            return []

        for tile in candidate_tiles:
            new_hand = current_hand + [tile]
            if self.is_hupai(new_hand):
                waiting.append(tile)

        return waiting



    def get_effective_tile(self, tile):
        """ 将宝牌显示的 '0s' 转换为实际牌，例如 '0s' → '5s' """
        if tile.startswith("0"):
            return "5" + tile[1:]
        return tile

    def get_possible_actions(self, tile, seat):
        """
        检测吃、碰、杠操作，返回所有可能的操作（不进行选择）。
        吃操作仅适用于数字牌（m, p, s）。
        """
        actions = []
        effective_tile = self.get_effective_tile(tile)


        # 碰：如果手中有两张相同的牌
        if self.hands.count(effective_tile) >= 2:
            actions.append({
                "type": 3,  # 3 表示碰
                "changeTiles": [],
                "changeTileStates": [],
                "gapType": 0,
                "combination": [f"{effective_tile}|{effective_tile}"]
            })

        # 杠：如果手中有三张相同的牌
        if self.hands.count(effective_tile) == 3:
            actions.append({
                "type": 5,  # 5 表示大明杠
                "changeTiles": [],
                "changeTileStates": [],
                "gapType": 0,
                "combination": [f"{effective_tile}|{effective_tile}|{effective_tile}"]
            })

        if seat == self.Myseat - 1 or (seat==3 and self.Myseat==0):
            # 吃：仅适用于数字牌（m, p, s）
            if len(effective_tile) > 1 and (effective_tile[1] in "mps"):
                try:
                    num = int(effective_tile[0])
                except ValueError:
                    num = 0
                suit = effective_tile[1]
                #0m等宝牌未考虑?0m在组合中是以5m代替显示的吗？
                if effective_tile[0] == "1" :
                    chi_combinations = [
                        {f"{num+1}{suit}", f"{num+2}{suit}"}
                    ]
                elif effective_tile[0] == "2" :
                    chi_combinations = [
                        {f"{num-1}{suit}", f"{num+1}{suit}"},
                        {f"{num+1}{suit}", f"{num+2}{suit}"}
                    ]
                else:
                    chi_combinations = [
                        {f"{num-2}{suit}", f"{num-1}{suit}"},
                        {f"{num-1}{suit}", f"{num+1}{suit}"},
                        {f"{num+1}{suit}", f"{num+2}{suit}"}
                    ]
                hand_copy = self.hands.copy()
                # for i in self.melds[self.Myseat]:
                #     print("i ",i)
                #     hand_copy.remove(i)
                # print("hand_copy ",hand_copy)
                doras = []
                for index, _ in enumerate(hand_copy) :
                    hand_copy.remove(_)
                    hand_copy.append(self.get_effective_tile(_))
                    if _ != self.get_effective_tile(_):
                        doras.append(_)

                self.myDoras=doras
                chi = []
                for chi_set in chi_combinations:
                    if chi_set.issubset(set(hand_copy)):  # 确保 chi_set 在手牌中
                        chi.append(list(chi_set)[0])
                        chi.append(list(chi_set)[1])

                if len(chi) == 2:
                    actions.append({
                        "type": 2,  # 2 表示吃
                        "changeTiles": [],
                        "changeTileStates": [],
                        "gapType": 0,
                        "combination": [f"{chi[0]}|{chi[1]}"]
                    })
                    #lastChi要在手牌中获取那些临近该组合的
                    # self.lastChi.append(effective_tile)
                elif len(chi) == 4:
                    actions.append({
                        "type": 2,  # 2 表示吃
                        "changeTiles": [],
                        "changeTileStates": [],
                        "gapType": 0,
                        "combination": [f"{chi[0]}|{chi[1]}", f"{chi[2]}|{chi[3]}"]
                    })
                    # self.lastChi.append(effective_tile)
                elif len(chi) == 6:
                    actions.append({
                        "type": 2,  # 2 表示吃
                        "changeTiles": [],
                        "changeTileStates": [],
                        "gapType": 0,
                        "combination": [
                            f"{chi[0]}|{chi[1]}",
                            f"{chi[2]}|{chi[3]}",
                            f"{chi[4]}|{chi[5]}"
                        ]
                    })
                    # self.lastChi.append(effective_tile)

        # 将检测到的操作更新到当前操作列表中
        if len(actions)>0:
            self.can_chipongang = True
            self.current_operationList = actions
        else:
            self.can_chipongang = False

        return

    def handle_discard(self, data):

        self.lastPlayer = self.currentPlayer
        self.currentPlayer = data.get("seat", self.Myseat)

        self.lastTile = self.currentTile
        self.currentTile = data.get("tile", "1m")

        self.current_operationList = []
        # self.can_chipongang = False
        doras = data.get("doras", [])
        if doras:
            self.doras = doras

        if data["state"] in ["GameStart", "GameEnd", "Other_cancel"]:
            return

        elif data["state"] == "MyAction_cancel":
            #己方取消吃碰杠，但是又轮到己方行动，那么就是"MyAction_cancel"+”"MyAction"连发
            self.clear_operations()
            return

        elif data["state"] == "Discard":
            seat = data["seat"]
            tile = data["tile"]

            self.discards[seat].append(tile)

            self.get_possible_actions(tile,seat)

            return

        elif data["state"] == "MyAction":

            tile = data["tile"]
            self.discards[self.Myseat].append(tile)

            if self.player[self.Myseat].get("is_liqi", False):
                data["state"] = "My_Liqi"
                return

            if data["getTile"] in ["0s","0p","0m"] :
                self.myDoras.append(data["getTile"])

            if data["tile"] in ["0s","0p","0m"] :
                self.myDoras.remove(data["tile"])

            self.handle_self_discard(data["tile"], data["getTile"])
            self.count_tingpaiList()

            if len(self.tingpai) > 0:
                self.can_liqi = True
                self.zhentingif(data["getTile"])
            return

        elif data["state"] == "MyAction_Chipongang":
            self.handle_self_chipongang(data)
            self.hands.remove(data["tile"])
            if data["operation"] == 2:
                self.updataForbiden(data)

            return

        elif data["state"] == "MyAction_Liqi":
            self.declare_liqi(data["seat"])
            self.liqiTodeal = data["tile_list"]
            # self.discards[self.Myseat].append(data["tile"])
            self.hands.append(data["getTile"])

            self.count_tingpaiList()

            return

        elif data["state"] == "Other_Chipongang":
            # 对手执行吃/碰/杠操作时，更新对手的明牌区
            seat = data["seat"]
            tile = data["tile"]
            operation = data.get("operation", {})

            self.get_possible_actions(tile,seat)
            self.discards[seat].append(tile)
            self.can_chipongang = False

            meld = [i for i in operation["combination"]]
            self.melds[seat].append(meld)

            if operation["type"] in [4,5,6]: #对手大明杠/暗杠/加杠
                self.doras.append(data["dora"])

            return

        elif data["type"] == "Other_liqi":
            seat = data["seat"]
            tile = data["tile"]
            self.discards[seat].append(tile)
            self.get_possible_actions(tile,seat)
            self.declare_liqi(data["seat"])
            return
        return

    def updataForbiden(self,data):
        for i in self.current_operationList:
            if i["type"] == 2:
                for j in i["combination"]:
                    for k in j.split("|"):
                        self.forbiden.append(k)
        return
    def LiqiJudge(self):
        """ 判断是否可以立直 """
        # 无吃碰杠，且有听牌，且未振听
        if self.melds:
            return False
        if len(self.tingpai) > 0:
            if not self.zhenting:
                return True

        return False

    def handle_self_discard(self, tile, gettile, tsumogiri=False):
        """ 处理己方出牌：从手牌中移除，并更新弃牌区 """
        self.hands.append(gettile)

        if tile in self.hands:
            self.hands.remove(tile)
        else:
            print(f"未持有 {tile}，当前手牌: {self.hands}")
            return

        self.tingpai = self.compute_tingpai(self.hands)
        self.is_furiten()

        self.can_liqi = self.LiqiJudge()

    def handle_self_chipongang(self, data):
        # if data["operation"]["type"] in [4 , 5, 6]:
        #     self.doras = data["doras"]

        self.can_chipongang = False
        self.hands.append(self.lastTile)
        for i in data["operation"]["combination"]:
            self.melds[self.Myseat].append(i)

            self.hands.remove(i)

        return


    def clear_operations(self):
        """ 清空待处理操作和当前操作列表 """
        self.can_chipongang = False
        self.current_operationList = []

    def get_ChiPengGang_flag(self):
        """ 返回是否有吃碰杠操作标志，依据当前操作列表 """
        return len(self.current_operationList)


    def declare_liqi(self, seat):
        """
        声明立直操作：
          - 更新该玩家的立直状态；
          - 若该玩家之前未立直，则全局立直棒数量加 1。
        """
        self.justLiqi = True

        if not self.player[seat].get("is_liqi", False):
            self.player[seat]["is_liqi"] = True
            self.liqibang += 1

        self.liqi_msg = self.get_liqi_msg()

        # if self.player[seat].get("zhenting", False):
        #     self.player[seat]["zhenting"] = False
    def get_liqi_msg(self):
        liqi_msg = []
        for i in range(4):
            if self.player[i].get("is_liqi", False):
                liqi_msg.append({
                    "score": 24000,
                    "liqibang": self.liqibang,
                    "seat": i,
                    "failed": False})
        return liqi_msg

    def cancel_liqi(self, seat):
        """
        取消立直状态：
          - 更新该玩家的立直状态；
          - 此处规则可能不允许取消后减少立直棒，这里仅输出提示信息。
        """
        if self.player.get(seat, {}).get("is_liqi", False):
            self.player[seat]["is_liqi"] = False
            print(f"🔕 玩家 {seat} 取消立直。")

    def end_game(self):
        """ 清空所有牌相关状态，重置为初始空值 """
        self.hands = []
        self.doras = []
        self.melds = {i: [] for i in range(4)}
        self.discards = {i: [] for i in range(4)}
        self.clear_operations()
        print("🔄 游戏结束，已清空所有牌局状态")

# 提供全局实例
tile_manager = TileManager(player_id=17457800)
