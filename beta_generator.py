import json
from beta_tileManager import tile_manager

global_msg_id = 0


def get_next_msg_id():
    """ 生成递增的消息 ID """
    global global_msg_id
    global_msg_id += 1
    return global_msg_id


def generate_liqi_msg(msg_type, method, data, id=None):
    """ 生成标准 LiqiMsg 格式，如果未指定 id 则自动生成递增 ID """
    if id is None:
        id = get_next_msg_id()
    return {
        "id": id,
        "type": msg_type,
        "method": method,
        "data": data
    }


def generate_auth_game_msg(seat_list):
    """
    生成符合标准的 .lq.FastTest.authGame 消息。
    - seat_list: 由 image_data["seatList"] 传入的座位顺序
    """

    default_names = ["VirtualPlayer1", "VirtualPlayer2", "VirtualPlayer3", "VirtualPlayer4"]  # 默认昵称
    players = []

    for i, account_id in enumerate(seat_list):
        player = {
            "accountId": account_id,
            "avatarId": 400101,
            "nickname": default_names[i] if i < len(default_names) else f"Player{i + 1}",
            "level": {"id": 10103, "score": 100 * (i + 1)},  # 假设分数不同
            "character": {
                "charid": 200001,
                "skin": 400101,
                "level": 0,
                "exp": 0,
                "views": [],
                "isUpgraded": False,
                "extraEmoji": [],
                "rewardedLevel": []
            },
            "level3": {"id": 20101 + i, "score": 0},
            "views": [{"slot": 13, "itemId": 0, "type": 0, "itemIdList": []}],
            "title": 0,
            "avatarFrame": 0,
            "verified": 0
        }
        players.append(player)
        # print(players)

    game_config = {
        "category": 2,
        "mode": {
            "mode": 1,
            "detailRule": {
                "timeFixed": 0,
                "timeAdd": 0,
                "doraCount": 0,
                "shiduan": 0,
                "initPoint": 0,
                "fandian": 0,
                "canJifei": False,
                "tianbianValue": 0,
                "liqibangValue": 0,
                "changbangValue": 0,
                "notingFafu1": 0,
                "notingFafu2": 0,
                "notingFafu3": 0,
                "haveLiujumanguan": False,
                "haveQieshangmanguan": False,
                "haveBiaoDora": False,
                "haveGangBiaoDora": False,
                "mingDoraImmediatelyOpen": False,
                "haveLiDora": False,
                "haveGangLiDora": False,
                "haveSifenglianda": False,
                "haveSigangsanle": False,
                "haveSijializhi": False,
                "haveJiuzhongjiupai": False,
                "haveSanjiahele": False,
                "haveToutiao": False,
                "haveHelelianzhuang": False,
                "haveHelezhongju": False,
                "haveTingpailianzhuang": False,
                "haveTingpaizhongju": False,
                "haveYifa": False,
                "haveNanruxiru": False,
                "jingsuanyuandian": 0,
                "shunweima2": 0,
                "shunweima3": 0,
                "shunweima4": 0,
                "bianjietishi": False,
                "aiLevel": 0,
                "haveZimosun": False,
                "disableMultiYukaman": False,
                "fanfu": 0,
                "guyiMode": 0,
                "dora3Mode": 0,
                "beginOpenMode": 0,
                "jiuchaoMode": 0,
                "muyuMode": 0,
                "openHand": 0,
                "xuezhandaodi": 0,
                "huansanzhang": 0,
                "chuanma": 0,
                "revealDiscard": 0,
                "fieldSpellMode": 0,
                "zhanxing": 0,
                "tianmingMode": 0,
                "disableLeijiyiman": False,
                "disableDoubleYakuman": 0,
                "disableCompositeYakuman": 0,
                "enableShiti": 0,
                "enableNontsumoLiqi": 0,
                "disableDoubleWindFourFu": 0,
                "disableAngangGuoshi": 0,
                "enableRenhe": 0,
                "enableBaopaiExtendSettings": 0,
                "yongchangMode": 0
            },
            "ai": False,
            "extendinfo": ""
        },
        "meta": {
            "modeId": 2,
            "roomId": 0,
            "contestUid": 0
        }
    }

    return generate_liqi_msg("MsgType.RES", ".lq.FastTest.authGame", {
        "players": players,
        "seatList": seat_list,
        "gameConfig": game_config,
        "isGameStart": False,
        "readyIdList": []
    })


def convert_image_data(image_data):
    """
    根据图像识别数据转换为标准 LiqiMsg。
    """

    tile_manager.handle_discard(image_data)

    state = image_data["state"]
    msgs = []
    step = tile_manager.step

    if state == "GameStart":
        tile_manager.initialize_game(image_data)

        seat_list = image_data.get("seatList")
        chang = image_data.get("chang", 0)
        # ben = seat_list.index(17457800)
        auth_req = generate_auth_game_msg(seat_list)

        enter_game_req = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.enterGame", {})
        confirm_req_id = get_next_msg_id() - 1
        enter_game_res = generate_liqi_msg("MsgType.RES", ".lq.FastTest.enterGame", {"isEnd": False, "step": 0},
                                           id=confirm_req_id)

        # confirm_req = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.confirmNewRound", {})
        # confirm_res = generate_liqi_msg("MsgType.RES", ".lq.FastTest.confirmNewRound", {})

        action_new_round = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step + 1,
            "name": "ActionNewRound",
            "data": {
                "tiles": tile_manager.hands,
                "scores": [25000, 25000, 25000, 25000],
                "leftTileCount": 69,
                "doras": tile_manager.doras,
                "opens": [{"seat": i, "tiles": [], "count": []} for i in range(4)],
                "sha256": "e0b876b10ae9f1661f934039f79bdc8cb5ee1b3b9ae52f6a0d842b2a79b2a8a6",
                "chang": chang,
                "ju": 0,
                "ben": 0,
                "dora": "",
                "liqibang": 0,
                "tingpais0": [],
                "tingpais1": [],
                "al": False,
                "md5": "",
                "juCount": 0,
                "fieldSpell": 0
            }

        }, id=-1)

        loadplayer_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.NotifyPlayerLoadGameReady", {"readyIdList": seat_list},id=-1)
        MJstart_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {"name": "ActionMJStart", "step": 0, "data": {}}, id=-1)

        fetch_state_req = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.fetchGamePlayerState", {})
        confirm_req_id = get_next_msg_id() - 1
        fetch_state_res = generate_liqi_msg("MsgType.RES", ".lq.FastTest.fetchGamePlayerState", {
            "stateList": ["READY", "READY", "READY", "READY"]
        }, id=confirm_req_id)

        tile_manager.step = step + 1
        msgs.extend([auth_req, enter_game_req, loadplayer_msg, enter_game_res, MJstart_msg, fetch_state_req, fetch_state_res, action_new_round])
        return msgs

    elif state == "MyAction":
        # 己方主动出牌，若有待处理操作则先取消

        tile = image_data["tile"]
        getTile = image_data["getTile"]

        seat = tile_manager.Myseat
        step = tile_manager.step

        moqie = False
        if tile == getTile:
            moqie = True

        #如果可以立直，则operationList中有liqi
        if tile_manager.can_liqi:
            tile_manager.leftTileCount -= 1
            deal_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionDealTile",
                "data": {
                    "seat": seat,
                    "tile": getTile,
                    "leftTileCount": tile_manager.leftTileCount,
                    "operation": {
                        "seat": seat,
                        "operationList": [{
                            "type": 1,
                            "combination": [],
                            "changeTiles": [],
                            "changeTileStates": [],
                            "gapType": 0}, {
                            "type": 7,
                            "combination": tile_manager.liqiTodeal,
                            "changeTiles": [],
                            "changeTileStates": [],
                            "gapType": 0}],
                        "timeAdd": 25000,
                        "timeFixed": 5000},
                    "tingpais": [
                        {
                        "tile": "5m",
                        "infos": [{
                            "tile": "7p",
                            "haveyi": True,
                            "count": 1,
                            "fu": 30,
                            "biaoDoraCount": 1,
                            "countZimo": 2,
                            "fuZimo": 20,
                            "yiman": False,
                            "yimanZimo": False
                        },
                        {
                            "tile": "4p",
                            "haveyi": True,
                            "count": 1,
                            "fu": 30,
                            "biaoDoraCount": 1,
                            "countZimo": 2,
                            "fuZimo": 20,
                            "yiman": False,
                            "yimanZimo": False
                        }
                        ],
                        "zhenting": False}],
                    "doras": [],
                    "zhenting": False,
                    "tileState": 0,
                    "tileIndex": 0}
            }, id=-1)
        else:
            tile_manager.leftTileCount -= 1
            deal_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionDealTile",
                "data": {
                    "tile": getTile,
                    "leftTileCount": tile_manager.leftTileCount,
                    "operation": {
                        "operationList": [
                            {
                                "type": 1,
                                "combination": [],
                                "changeTiles": [],
                                "changeTileStates": [],
                                "gapType": 0}
                        ],
                        "timeAdd": 20000,
                        "timeFixed": 5000,
                        "seat": seat},
                    "seat": seat,
                    "doras": [],
                    "zhenting": tile_manager.zhenting,
                    "tingpais": tile_manager.tingpai,
                    "tileState": 0,
                    "tileIndex": 0}
            }, id=-1)


        # if len(tile_manager.tingpai)>0 :   #听牌是指只差一张牌，并非牌距
        #     tingpai_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
        #         "step": 69,
        #         "name": "ActionDiscardTile",
        #         "data": {
        #             "tile": "1z",
        #             "moqie": True,
        #             "tingpais": tile_manager.tingpai,
        #             "seat": 0,
        #             "isLiqi": tile_manager.player[seat]['is_liqi'],
        #             "zhenting": False,
        #             "doras": [],
        #             "isWliqi": False,
        #             "tileState": 0,
        #             "revealed": False,
        #             "scores": [],
        #             "liqibang": 0
        #         }
        #     }, id=-1)
        #     step += 1

        req_msg = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.inputOperation", {
            "type": 1,
            "tile": tile,
            "timeuse": 2,
            "index": 0,
            "cancelOperation": False,
            "moqie": moqie,
            "tileState": 0,
            "changeTiles": [],
            "tileStates": [],
            "gapType": 0
        })

        confirm_req_id = get_next_msg_id() - 1
        res_msg = generate_liqi_msg("MsgType.RES", ".lq.FastTest.inputOperation", {}, id=confirm_req_id)


        discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step + 1,
            "name": "ActionDiscardTile",
            "data":{
                "seat": seat,
                "tile": tile,
                "moqie": moqie,
                "isLiqi": False,
                "zhenting": False,
                "tingpais": [],
                "doras": [],
                "isWliqi": False,
                "tileState": 0,
                "revealed": False,
                "scores": [],
                "liqibang": 0
        }}, id=-1)


        tile_manager.step = step + 2

        msgs.extend([deal_msg, req_msg, res_msg, discard_msg])

        return msgs

    elif state == "My_Liqi":
        #立直状态后全是摸切
        tile = image_data["tile"]
        step = tile_manager.step
        getTile = image_data["getTile"]
        seat = tile_manager.Myseat

        tile_manager.leftTileCount -= 1

        mopai_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step,
            "name": "ActionDealTile",
            "data":{
                "seat": seat,
                "tile": getTile,
                "leftTileCount": tile_manager.leftTileCount,
                "operation": {
                    "seat": seat,
                    "timeAdd": 16000,
                    "timeFixed": 5000,
                    "operationList": []},
                "tingpais": [{
                    "tile": tile,
                    "infos": [{"tile": "7p", "haveyi": True, "count": 2, "fu": 30, "biaoDoraCount": 1, "countZimo": 3, "fuZimo": 20, "yiman": False, "yimanZimo": False},
                              {"tile": "4p", "haveyi": True, "count": 2, "fu": 30, "biaoDoraCount": 1, "countZimo": 3, "fuZimo": 20, "yiman": False, "yimanZimo": False}],
                    "zhenting": tile_manager.zhenting}],
                "doras": tile_manager.myDoras,
                "zhenting": tile_manager.zhenting,
                "tileState": 0,
                "tileIndex": 0
            }}, id=-1)



        discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step+1,
            "name": "ActionDiscardTile",
            "data":{
                "seat": seat,
                "tile": tile,
                "moqie": True,
                "tingpais": [{"tile": "7p", "haveyi": True, "count": 2, "fu": 30, "biaoDoraCount": 1, "countZimo": 3, "fuZimo": 20, "yiman": False, "yimanZimo": False},
                             {"tile": "4p", "haveyi": True, "count": 2, "fu": 30, "biaoDoraCount": 1, "countZimo": 3, "fuZimo": 20, "yiman": False, "yimanZimo": False}],
                "isLiqi": False,
                "zhenting": False,
                "doras": tile_manager.myDoras,
                "isWliqi": False,
                "tileState": 0,
                "revealed": False,
                "scores": [],
                "liqibang": 0
            }}, id=-1)

        tile_manager.step = step + 2
        msgs.extend([mopai_msg, discard_msg])

        return msgs

    elif state == "Discard":

        seat = image_data["seat"]
        tile = image_data["tile"]

        tile_manager.leftTileCount -= 1

        operationList = tile_manager.current_operationList

        if not tile_manager.justLiqi:
            mopai_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionDealTile",
                "data": {
                    "leftTileCount": tile_manager.leftTileCount,
                    "seat": seat,
                    "tile": "",
                    "doras": [],
                    "zhenting": False,
                    "tingpais": [],
                    "tileState": 0,
                    "tileIndex": 0
                }
            }, id=-1)

        else:
            liqi_msg = tile_manager.liqi_msg
            mopai_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionDealTile",
                "data": {
                    "leftTileCount": tile_manager.leftTileCount,
                    "seat": seat,
                    "liqi": liqi_msg ,
                    "tile": "",
                    "doras": [],
                    "zhenting": False,
                    "tingpais": [],
                    "tileState": 0,
                    "tileIndex": 0
                }
            }, id=-1)


        flag = tile_manager.get_ChiPengGang_flag()

        if flag > 0:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "seat": seat,
                    "tile": tile,
                    "operation": {
                        "operationList": operationList,
                        "timeAdd": 20000,
                        "timeFixed": 5000
                    },
                    "moqie": True,
                    "isLiqi": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": tile_manager.liqibang
                }
            }, id=-1)
        else:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "seat": seat,
                    "tile": tile,
                    "isLiqi": False,
                    "moqie": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": 0
                    }
                },id=-1)

        if step == 1:
            msgs.append(discard_msg)
        else:
            msgs.extend([mopai_msg,discard_msg])

        tile_manager.justLiqi = False
        tile_manager.step = step + 2
        return msgs

    elif state == "MyAction_cancel":
        timeuse = 2
        #仅限于吃/碰/大明杠的取消
        req_messages = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.inputChiPengGang", {
            "cancelOperation": True,
            "timeuse": timeuse,
            "type": 0,
            "index": 0
        })
        res_id = get_next_msg_id() - 1
        res_messages = generate_liqi_msg("MsgType.RES", ".lq.FastTest.inputChiPengGang", {}, id=res_id)
        msgs.extend([req_messages, res_messages])
        return msgs

    elif state == "Other_cancel":      #暂不考虑
        step = tile_manager.step
        notify_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step,
            "name": "ActionCancel",
            "data": {}
        }, id=-1)
        tile_manager.step = step + 1
        msgs.append(notify_msg)
        return

    elif state == "MyAction_Chipongang":
        # 己方吃碰杠操作，生成请求／应答及通知消息
        step = tile_manager.step
        seat = tile_manager.Myseat
        operation = image_data["operation"]


        if operation["type"] in [4,6]:   #暗杠加杠需要不同处理
            req_msg = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.inputOperation", {
                "type": operation["type"],
                "timeuse": 1,
                "cancelOperation": False,
                "index": 0
            })

            res_id = get_next_msg_id() - 1
            res_msg = generate_liqi_msg("MsgType.RES", ".lq.FastTest.inputOperation", {}, id=res_id)

            notify_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionAnGangAddGang",
                "data": {
                    "type": 3,
                    "tiles": list(set(operation["combination"]))[0],
                    "seat": seat,
                    "doras": [],
                    "zhenting": tile_manager.zhenting,
                    "tingpais": tile_manager.tingpai
                }}, id=-1)

        else:
            req_msg = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.inputChiPengGang", {
                "type": operation["type"],
                "timeuse": 1,
                "cancelOperation": False,
                "index": 0,
                "moqie": False,
                "tileState": 0,
                "changeTiles": [],
                "tileStates": [],
                "gapType": 0
            })

            res_id = get_next_msg_id() - 1
            res_msg = generate_liqi_msg("MsgType.RES", ".lq.FastTest.inputChiPengGang", {}, id=res_id)

            notify_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step,
                "name": "ActionChiPengGang",
                "data": {
                    "tiles": operation["combination"],
                    "froms": operation["form"],
                    "operation": {
                        "operationList": [{
                        "type": 1,
                        "combination": operation["tile_list"],
                        "changeTiles": [],
                        "changeTileStates": [],
                        "gapType": 0}],
                     "timeAdd": 20000,
                     "timeFixed": 5000,
                     "seat": seat},
                 "tileStates": [0, 0],
                 "seat": seat,
                 "type": 0,
                 "zhenting": tile_manager.get("zhenting", False),
                 "tingpais": tile_manager.get("tingpai", []),
                 "scores": [],
                 "liqibang": 0 }}, id=-1)

        tile_manager.step = step + 1
        msgs.extend([req_msg, res_msg, notify_msg])
        return msgs

    elif state == "MyAction_liqi":
        getTile = image_data["getTile"]
        step = tile_manager.step
        seat = tile_manager.Myseat
        tile = image_data["tile"]

        tile_manager.leftTileCount -= 1
        deal_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
        "step": step,
        "name": "ActionDealTile",
        "data": {
            "tile": getTile,
            "leftTileCount": tile_manager,
            "operation": {
                "operationList": [
                    {
                    "type": 1,
                    "combination": [],
                    "changeTiles": [],
                    "changeTileStates": [],
                    "gapType": 0},
                    {
                    "type": 7,
                    "combination": tile_manager.liqiTodeal,
                    "changeTiles": [],
                    "changeTileStates": [],
                    "gapType": 0}],
               "timeAdd": 20000,
               "timeFixed": 5000,
               "seat": seat},
               "tingpais": tile_manager.tingpai ,
               "seat": seat,
               "doras": tile_manager.myDoras,
               "zhenting": False,
               "tileState": 0,
               "tileIndex": 0}}, id=-1)

        req_msg = generate_liqi_msg("MsgType.REQ", ".lq.FastTest.inputOperation", {
            "type": 7,
            "tile": tile,
            "timeuse": 2,
            "index": 0,
            "cancelOperation": False,
            "moqie": False,
            "tileState": 0,
            "changeTiles": [],
            "tileStates": [],
            "gapType": 0
        })
        confirm_req_id = get_next_msg_id() - 1
        res_msg = generate_liqi_msg("MsgType.RES", ".lq.FastTest.inputOperation", {}, id=confirm_req_id)

        tile_manager.step = step + 1
        msgs.extend([deal_msg, req_msg, res_msg])
        return msgs




    elif state == "Other_Chipongang":
        step = tile_manager.step
        seat = image_data["seat"]
        operation = image_data["operation"]
        tile = image_data["tile"]

        notify_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step,
            "name": "ActionChiPengGang",
            "data": {
                "seat": seat,
                "tiles": operation.get("combination", []),
                "froms": operation.get("form", []),
                "tileStates": [0, 0],
                "type": operation["type"]-2 ,
                "zhenting": False,
                "tingpais": [],
                "scores": [],
                "liqibang": 0
            }
        }, id=-1)

        chipongang_flag = tile_manager.get_ChiPengGang_flag()

        if chipongang_flag == 0:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "tile": tile,
                    "seat": seat,
                    "isLiqi": False,
                    "moqie": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": 0
                }
            }, id=-1)
        else:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "seat": seat,
                    "tile": tile,
                    "operation": {
                        "operationList": tile_manager.current_operationList
                    },
                    "isLiqi": False,
                    "moqie": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": 0
                }
            }, id=-1)
        tile_manager.step = step + 2
        msgs.extend([notify_msg, discard_msg])
        return msgs

    elif state == "Other_liqi":
        step = tile_manager.step
        seat = image_data["seat"]
        tile = image_data["tile"]

        tile_manager.leftTileCount -= 1
        mopai_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
            "step": step,
            "name": "ActionDealTile",
            "data": {
                "leftTileCount": tile_manager.leftTileCount,
                "seat": seat,
                "tile": "",
                "doras": [],
                "zhenting": False,
                "tingpais": [],
                "tileState": 0,
                "tileIndex": 0
            }
        }, id=-1)

        chipongang_flag = tile_manager.get_ChiPengGang_flag()

        if chipongang_flag == 0:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "tile": tile,
                    "isLiqi": True,
                    "seat": seat,
                    "moqie": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": 0
                }
            }, id=-1)
        else:
            discard_msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.ActionPrototype", {
                "step": step + 1,
                "name": "ActionDiscardTile",
                "data": {
                    "seat": seat,
                    "tile": tile,
                    "isLiqi": True,
                    "operation": {
                        "operationList": tile_manager.current_operationList,
                        "timeAdd": 20000,
                        "timeFixed": 5000
                    },
                    "moqie": False,
                    "zhenting": False,
                    "tingpais": [],
                    "doras": [],
                    "isWliqi": False,
                    "tileState": 0,
                    "revealed": False,
                    "scores": [],
                    "liqibang": 0
                }
            }, id=-1)

        tile_manager.step = step + 2
        msgs.extend([mopai_msg, discard_msg])
        return msgs

    elif state == "GameEnd":
        tile_manager.end_game()
        msg = generate_liqi_msg("MsgType.NOTIFY", ".lq.NotifyGameEndResult", {
            "step": -1,
            "name": "ActionHule",
            "data": {}
        }, id=-1)
        msgs.append(msg)
        return msgs

    return None
