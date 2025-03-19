start = {
'''LiqiMsg: {"id": 1, "type": "MsgType.RES", "method": ".lq.FastTest.authGame", "data": {"players": [{"accountId": 17457800, "avatarId": 400101, "nickname": "猫机", "level": {"id": 10101, "score": 18}, "character": {"charid": 200001, "exp": 200, "skin": 400101, "level": 0, "views": [], "isUpgraded": false, "extraEmoji": [], "rewardedLevel": []}, "level3": {"id": 20101, "score": 0}, "title": 0, "avatarFrame": 0, "verified": 0, "views": []}], "seatList": [13, 17457800, 11, 12], "gameConfig": {"category": 1, "mode": {"mode": 3, "ai": true, "detailRule": {"timeFixed": 5, "timeAdd": 20, "doraCount": 3, "shiduan": 1, "initPoint": 25000, "fandian": 30000, "bianjietishi": true, "aiLevel": 1, "fanfu": 1, "canJifei": false, "tianbianValue": 0, "liqibangValue": 0, "changbangValue": 0, "notingFafu1": 0, "notingFafu2": 0, "notingFafu3": 0, "haveLiujumanguan": false, "haveQieshangmanguan": false, "haveBiaoDora": false, "haveGangBiaoDora": false, "mingDoraImmediatelyOpen": false, "haveLiDora": false, "haveGangLiDora": false, "haveSifenglianda": false, "haveSigangsanle": false, "haveSijializhi": false, "haveJiuzhongjiupai": false, "haveSanjiahele": false, "haveToutiao": false, "haveHelelianzhuang": false, "haveHelezhongju": false, "haveTingpailianzhuang": false, "haveTingpaizhongju": false, "haveYifa": false, "haveNanruxiru": false, "jingsuanyuandian": 0, "shunweima2": 0, "shunweima3": 0, "shunweima4": 0, "haveZimosun": false, "disableMultiYukaman": false, "guyiMode": 0, "dora3Mode": 0, "beginOpenMode": 0, "jiuchaoMode": 0, "muyuMode": 0, "openHand": 0, "xuezhandaodi": 0, "huansanzhang": 0, "chuanma": 0, "revealDiscard": 0, "fieldSpellMode": 0, "zhanxing": 0, "tianmingMode": 0, "disableLeijiyiman": false, "disableDoubleYakuman": 0, "disableCompositeYakuman": 0, "enableShiti": 0, "enableNontsumoLiqi": 0, "disableDoubleWindFourFu": 0, "disableAngangGuoshi": 0, "enableRenhe": 0, "enableBaopaiExtendSettings": 0, "yongchangMode": 0}, "extendinfo": ""}, "meta": {"roomId": 10143, "modeId": 0, "contestUid": 0}}, "readyIdList": [13, 11, 12], "isGameStart": false}}
==================================================
LiqiMsg: {"id": 3, "type": "MsgType.REQ", "method": ".lq.FastTest.enterGame", "data": {}}
==================================================
LiqiMsg: {"id": -1, "type": "MsgType.NOTIFY", "method": ".lq.NotifyPlayerLoadGameReady", "data": {"readyIdList": [13, 17457800, 11, 12]}}
==================================================
LiqiMsg: {"id": 3, "type": "MsgType.RES", "method": ".lq.FastTest.enterGame", "data": {"isEnd": false, "step": 0}}
==================================================
LiqiMsg: {"id": -1, "type": "MsgType.NOTIFY", "method": ".lq.ActionPrototype", "data": {"name": "ActionMJStart", "step": 0, "data": {}}}
==================================================
LiqiMsg: {"id": 4, "type": "MsgType.REQ", "method": ".lq.FastTest.fetchGamePlayerState", "data": {}}
==================================================
LiqiMsg: {"id": 4, "type": "MsgType.RES", "method": ".lq.FastTest.fetchGamePlayerState", "data": {"stateList": ["READY", "READY", "READY", "READY"]}}
'''
}

real_start={
'''==================================================
LiqiMsg: {
    "id": -1, 
    "type": "MsgType.NOTIFY", 
    "method": ".lq.ActionPrototype", 
    "data": {
        "step": 1, 
        "name": "ActionNewRound", 
        "data": {
            "tiles": ["8p", "5m", "7s", "9m", "7s", "5s", "7m", "0m", "4z", "2p", "3p", "7m", "4p"], 
            "scores": [25000, 25000, 25000, 25000], 
            "leftTileCount": 69, 
            "doras": ["7m"], 
            "opens": [{"seat": 0, "tiles": [], "count": []}, 
            {"seat": 1, "tiles": [], "count": []}, 
            {"seat": 2, "tiles": [], "count": []}, 
            {"seat": 3, "tiles": [], "count": []}], 
            "sha256": "e0b876b10ae9f1661f934039f79bdc8cb5ee1b3b9ae52f6a0d842b2a79b2a8a6", 
            "chang": 0, 
            "ju": 0, 
            "ben": 0, 
            "dora": "", 
            "liqibang": 0, 
            "tingpais0": [], 
            "tingpais1": [], 
            "al": false, "md5": "", "juCount": 0, "fieldSpell": 0}}}
=================================================='''
}