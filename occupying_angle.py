def play(statu, storage):
    '''
    主函数：简单占角
    逻辑:
    按照记录最开始位置, 然后到最近角占角, 占了最接近两角后就有圈内游走

    输入：
       游戏数据stat, 记录行走走骤storage['stepp']
    输出：
        行动''L', 'R', 'S'
    '''
    stat = statu['now']
    gameLog = statu['log']
    me = stat['me']
    me_d = me['direction']
    id = stat['me']['id']
    turnlist = ['R', 'L']
    x = statu['size'][0] - 1
    y = statu['size'][1] - 1
    x_1 = gameLog[0]['me']['x'] - 1
    y_1 = gameLog[0]['me']['y'] - 1
    me_x, me_y = stat['me']['x'], stat['me']['y']
    ene_d = stat['enemy']['direction']
    if not 'stepp' in storage:
        storage['stepp'] = 0
    stepp = storage['stepp'] % 8
    if stepp <= 3:
        if stepp <=2:
            storage['stepp'] += 1
            return 'S'
        elif (me_d == 0 and id == 1) or (id == 2 and me_d == 2):
            storage['stepp'] += 1
            return 'L'
        else:
            storage['stepp'] += 1
            return 'S'
    else:
        if stepp == 4:
            if me_d == 3 and me_y == 1:
                storage['stepp'] += 1
                return turnlist[(id) % 2]
            elif me_d == 1 and me_y == y:
                storage['stepp'] += 1
                return turnlist[(id+1) % 2]
            elif (me_d == 0 and me_x == x) or (me_d == 2 and me_x == 1):
                storage['stepp'] += 1
                if stat['enemy']['x'] <= (me_x // 2):
                    return turnlist[(id + 1) % 2]
                return turnlist[id % 2]
            else:
                return 'S'
        elif stepp == 5:
            if (me_x == 1 and me_y == 1) or (me_x == x and me_y == y):
                storage['stepp'] += 1
                return 'L'
            elif (me_x == x and me_y == 1) or (me_x== 1 and me_y == y):
                storage['stepp'] += 1
                return 'R'
            else:
                return 'S'
        elif stepp == 6:
            if (me_d == 1 or me_d == 3) and me_y == y_1+1:
                storage['stepp'] += 1
                if me_d == 3:
                    return turnlist[(id+1)%2]
                return turnlist[id%2]
            return 'S'
        elif me_y == y_1+1 and me_x == x_1:
            storage['stepp'] += 1
            return turnlist[((storage['stepp']+1)//8)%2]
        else:
            return 'S'

