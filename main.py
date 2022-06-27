import sys, random
sys.path.append('../..')
import go
import plugins.groupadmin.main as groupadmin

def langrensha(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    print('init langrensha')
    lrs1 = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    # lrs = lrs1[0]
    if isinstance(lrs1, tuple):
        go.commonx('INSERT INTO `botLangrensha` (`qn`) VALUES ('+str(gid)+')')
    go.send(meta_data, '[CQ:face,id=151] 开始狼人杀，已创建房间，等待加入...')
    
def stateLrs(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    state = checkLrs(gid)
    if state == 1:
        go.send(meta_data, '本群还没有开始，请发送 开始狼人杀 以开始')
    elif state == 2:
        go.send(meta_data, '人数不够，再来点~')
    elif state == 3:
        go.send(meta_data, '可以开始，请发送 开始游戏 以开始')

def checkLrs(gid):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    lrs1 = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    lrs = lrs1[0]
    if isinstance(lrs, tuple):
        return 1
    else:
        lenn = len(lrs)-2
        while lenn > 0:
            if lrs.get(lenn) == '0':
                return 2
            lenn -= 1
        return 3
        
def getLrs(num):
    arr = ['预言家','守卫','女巫','猎人','狼1','狼2','狼3','白狼王','民1','民2','民3','民4']
    return arr[num-1]

def addLrs(meta_data):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    print('addLrs')
    global LrsAddNum
    rand = random.randint(1, LrsAddNum)
    listtt = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    listt = listtt[0]
    i = 0
    l = 0
    while i <= len(listt):
        if listt.get(str(i)) == 0:
            l += 1
        if l == rand:
            go.commonx('UPDATE `botLangrensha` SET `'+str(i)+'`='+str(uid))
            go.SendOld(uid, '您的身份：'+getLrs(i))
            go.send(meta_data, '已分配身份，若没收到私聊，请先添加机器人好友！')
            break
        # print('i:'+str(i)+' rand:'+str(rand)+' l:'+str(l))
        i += 1
    LrsAddNum -= 1

def startLrs(meta_data, jvshu=1):
    uid = meta_data.get('se').get('user_id')
    gid = meta_data.get('se').get('group_id')
    
    global killFlag, killList, tpList
    print('start lrs')
    go.send(meta_data, '开始狼人杀~\n全员禁言')
    meta_data['message'] = 'true'
    groupadmin.muteall(meta_data, 'false')
    go.send(meta_data, '第'+str(jvshu)+'夜~')
    
    listtt = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    listt = listtt[0]
    
    if listt.get('5') == '0' and listt.get('6') == '0' and listt.get('7') == '0' and listt.get('8') == '0':
        go.send(meta_data, '狼人全部死了，游戏结束~')
    else:
        go.send(meta_data, '请狼人杀人')
        # 狼人
        go.send(listt.get('5'), '[上帝] 请与其他狼人商讨并选择要杀的玩家，并回复：击杀|'+str(gid)+'|<要杀的玩家的qq号>\n其他狼人：'+str(listt.get('6'))+'/'+str(listt.get('7'))+'/'+str(listt.get('8')))
        go.send(listt.get('6'), '[上帝] 请与其他狼人商讨并选择要杀的玩家，并回复：击杀|'+str(gid)+'|<要杀的玩家的qq号>\n其他狼人：'+str(listt.get('5'))+'/'+str(listt.get('7'))+'/'+str(listt.get('8')))
        go.send(listt.get('7'), '[上帝] 请与其他狼人商讨并选择要杀的玩家，并回复：击杀|'+str(gid)+'|<要杀的玩家的qq号>\n其他狼人：'+str(listt.get('6'))+'/'+str(listt.get('5'))+'/'+str(listt.get('8')))
        go.send(listt.get('8'), '[上帝] 请与其他狼人商讨并选择要杀的玩家，并回复：击杀|'+str(gid)+'|<要杀的玩家的qq号>\n其他狼人：'+str(listt.get('6'))+'/'+str(listt.get('7'))+'/'+str(listt.get('5')))
        
        # 等待击杀
        while killFlag == 0:
            continue
        killFlag = 0
    
    if listt.get('3') != '0':
        go.send(meta_data, '请女巫行使技能')
        go.send(listt.get('3'), '[上帝] 请女巫使用技能\n杀人请回复：击杀|'+str(gid)+'|<要杀的玩家的qq号>\n救人请回复：救人|'+str(gid)+'|<要救的玩家的qq号>')
        
        while killFlag == 0:
            continue
        killFlag = 0
    
    if listt.get('2') != '0':
        go.send(meta_data, '请守卫行使技能')
        go.send(listt.get('2'), '[上帝] 请守卫使用技能\n救人请回复：救人|'+str(gid)+'|<要救的玩家的qq号>')
        
        while killFlag == 0:
            continue
        killFlag = 0
    
    if listt.get('1') != '0':
        go.send(meta_data, '请预言家查身份')
        go.send(listt.get('1'), '[上帝] 请查询身份，回复：查询|'+str(gid)+'|<要查的人的qq号>')
        
        while killFlag == 0:
            continue
        killFlag = 0
    
    go.send(meta_data, '天亮了~')
    # 公布死亡
    deathmessage = '死亡的人：'
    l = 0
    for i in killList:
        if str(i.get('qn')) == str(gid):
            go.commonx('UPDATE `botLangrensha` SET `'+str(selrs(gid, i.get('killid')))+'`=0 WHERE `qn`='+str(gid))
            deathmessage += ' [CQ:at,qq='+str(i.get('killid'))+']'
            killList.pop(l)
        l += 1
            
    go.send(meta_data, deathmessage)
    groupadmin.muteall(uid, gid, 'false', 'false')
    go.send(meta_data, '你们有5分钟的时间讨论，白狼王和猎人可随时发送：自爆|'+str(gid)+'|<要带走的人的qq号>\n投票请私聊对我说：投票|'+str(gid)+'|<要投的人的qq号>')
    
    listtt = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    listt = listtt[0]
    summ = 0
    for i in listt:
        if isinstance(i, int) and listt.get(str(i)) != '0':
            summ += 1
    
    times = 0
    zbFlag = 0
    while times < 10:
        if killFlag == 1:
            zbFlag = 1
            break 
        time.sleep(1)
        times += 1
    
    if zbFlag == 0:
        minnuid = 0
        minnsum = 0
        for i in tpList:
            if str(i.get('qn')) == str(gid) and int(i.get('sum')) > minnsum:
                minnsum = int(i.get('sum'))
                minnuid = i.get('uid')
        if minnuid != 0:
            go.commonx('UPDATE `botLangrensha` SET `'+str(selrs(gid, minnuid))+'`=0 WHERE `qn`='+str(gid))
            go.send(meta_data, '投票结束~\n[CQ:at,qq='+str(minnuid)+'] 出局')
        return startLrs(meta_data, jvshu+1)

def tpLrs(meta_data):
    uid = meta_data.get('se').get('user_id')
    message = meta_data.get('message')
    
    global tpList, tpSum
    flag = 0
    message1 = message.split('|')
    gid = message1[0]
    playerid = message1[1]
    l = 0
    for i in tpList:
        if str(i.get('qn')) == str(gid) and str(i.get('uid')) == str(playerid):
            tpList[l]['sum'] += 1
            flag = 1
        l += 1
    if flag == 0:
        tpList.append({'qn':gid, 'uid':playerid, 'sum':1})
    go.SendOld(uid, 'Got it!')

def selrs(gid, playerid):
    listtt = go.selectx('SELECT * FROM `botLangrensha` WHERE `qn`='+str(gid))
    listt = listtt[0]
    i = 1
    while i <= len(listt):
        if str(listt.get(str(i))) == str(playerid):
            return i
        i += 1
    return -1

def searchPlayer(uid, message):
    global killFlag
    message1 = message.split('|')
    gid = message1[0]
    playerid = message1[1]
    res = selrs(gid, playerid)
    if res == -1:
        go.SendOld(uid, '没有查到~')
    else:
        go.SendOld(uid, getLrs(res))
    killFlag = 1

def savePlayer(uid, message):
    global killFlag, killList
    message1 = message.split('|')
    gid = message1[0]
    killid = message1[1]
    l = 0
    for i in killList:
        if i.get('killid') == killid:
            break
        else:
            l += 1
    print(l)
    killList.pop(l)
    killFlag = 1
    go.SendOld(uid, 'Got it!')

def killPlayer(uid, message):
    global killFlag, killList
    message1 = message.split('|')
    gid = message1[0]
    killid = message1[1]
    killList.append({'qn':gid, 'killid':killid})
    killFlag = 1
    go.SendOld(uid, 'Got it!')

# ------狼人杀----------
LrsAddNum = 12
killFlag = 0
killList = []
tpList = []