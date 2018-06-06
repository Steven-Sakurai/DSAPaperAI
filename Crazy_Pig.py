'''

stat: 
    size = [width, height]
    log = list(dict)
    now

    inside the dict:
        turnleft = [先手，后手]
        timeleft
        fields[i][j]   1, 2, None
        bands[i][j]    1, 2, None
        players = [先手玩家信息，后手]
        me
        enemy
            玩家信息：
                id: 1, 2
                x, y
                direction: 0, 1, 2, 3
'''


def play(stat, storage):
    curr_mode = storage[storage['mode']]
    field, me = stat['now']['fields'], stat['now']['me']
    storage['enemy'] = stat['now']['enemy']
    storage['Update'](stat, storage)
    return curr_mode(field, me, storage)


def load(stat, storage):
    # 基础设施准备
    import numpy as np  
    from random import choice, randrange
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    right = np.array([[0, 1], [-1, 0]])
    left = np.array([[0, -1], [1, 0]])
    
    size, field, band, me = stat['size'], stat['now']['fields'], stat['now']['bands'], stat['now']['me']
    myOrder = me['id'] # 1, 2 
    storage['myField'] = np.zeros([size[0], size[1]])
    myField = np.zeros([size[0], size[1]])
    # 0: nothing, 1: my field, 2: my band, 3: his field, 4: his band

    def update_myField(stat, storage):
        size, field, band = stat['size'], stat['now']['fields'], stat['now']['bands']
        myField = np.zeros([size[0], size[1]])
        for i in range(size[0]):
            for j in range(size[1]):
                if band[i][j] is None:
                    continue
                elif band[i][j] == myOrder:
                    myField[i, j] = 2
                else:
                    myField[i, j] = 4

                if field[i][j] is None:
                    continue
                elif field[i][j] == myOrder:
                    myField[i, j] = 1
                else:
                    myField[i, j] = 3
        storage['myField'] = myField
        enemy_pos = np.array([stat['now']['enemy']['x'], stat['now']['enemy']['y']])
        my_pos = np.array([stat['now']['me']['x'], stat['now']['me']['y']])
        storage['my_pos'] = my_pos
        storage['enemy_pos'] = enemy_pos 
        return

    storage['Update'] = update_myField

    for i in range(size[0]):
        for j in range(size[1]):
            if band[i][j] is None:
                continue
            elif band[i][j] == myOrder:
                myField[i, j] = 2
            else:
                myField[i, j] = 4

            if field[i][j] is None:
                continue
            elif field[i][j] == myOrder:
                myField[i, j] = 1
            else:
                myField[i, j] = 3
    storage['myField'] = myField

    # 计算安全距离
    def dist(me, enemy, conserv=5):
        return max(2, (abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//conserv)

    def wander(field, me, storage):
        # 防止出界
        # x轴不出界
        enemy_pos = storage['enemy_pos']
        my_pos = storage['my_pos']
        dir_now = directions[me['direction']]
        dist_now = np.sum(np.abs(my_pos - enemy_pos))
        dist_next = np.zeros([2, 1])
        for d in ['l', 'r']:
            if d == 'l':
                dir_next = np.matmul(left, dir_now)
                my_pos_tmp = my_pos + dir_next
                dist_next[0] = np.sum(np.abs(my_pos_tmp - enemy_pos))
            elif d == 'r':
                dir_next = np.matmul(right, dir_now)
                my_pos_tmp = my_pos + dir_next
                dist_next[1] = np.sum(np.abs(my_pos_tmp - enemy_pos)) 
        
        prefered_dir = None
        dirs = ['l', 'r']
        if dist_next[0] > dist_next[1]:
            prefered_dir = 0
        else:
            prefered_dir = 1

        if dist_now < 20:
            prefered_dir = (prefered_dir + 1) % 2

        nextx = me['x'] + directions[me['direction'], 0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = choice('rl')
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nextx <= 1) ^ (me['direction'] == 1)]

        # y轴不出界
        nexty = me['y'] + directions[me['direction'], 1]
        if nexty <= 1 and me['direction'] != 1 or nexty >= len(
                field[0]) - 2 and me['direction'] != 3:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2:  # 掉头
                next_turn = dirs[prefered_dir]
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = dirs[prefered_dir]
            storage['maxl'] = dist(me, storage['enemy'])
            return ''

        # 随机前进，转向频率递减
        if randrange(storage['count']) == 0:
            storage['count'] += 3
            return dirs[prefered_dir]

    # 领地外画圈
    def square(field, me, storage):
        # 防止出界
        if me['direction'] % 2:  # y轴不出界
            nexty = me['y'] + directions[me['direction'], 1]
            if nexty < 0 or nexty >= len(field[0]):
                storage['count'] = 0
                return storage['turn']
        else:  # x轴不出界
            nextx = me['x'] + directions[me['direction'], 0]
            if nextx < 0 or nextx >= len(field):
                storage['count'] = 0
                return storage['turn']

        # 状态转换
        if field[me['x']][me['y']] == me['id']:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return

        # 画方块
        storage['count'] += 1
        if storage['count'] >= storage['maxl']:
            storage['count'] = 0
            return storage['turn']

    # 返回领地中心
    def goback(field, me, storage):
        # 第一步掉头
        if storage['turn']:
            res, storage['turn'] = storage['turn'], None
            return res

        # 状态转换
        elif field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)

            myField = storage['myField']
            my_pos = storage['my_pos']
            hisPos = storage['enemy_pos']
            hisDist = np.sum(np.abs(my_pos - hisPos))
    
            enemy_field = np.c_[np.where(myField == 3)]
            min_dis = 10000
            for ep in enemy_field:
                thedis = np.sum(np.abs(ep - my_pos))
                if thedis < min_dis:
                    min_dis = thedis
            if hisDist < 10:
                conserv = 6
            elif min_dis < hisDist / 8:
                conserv = 3
            elif min_dis < hisDist / 4:
                conserv = 4
            else:
                conserv = 5
            storage['maxl'] = dist(me, storage['enemy'], conserv)
            storage['turn'] = choice('rl')
            return ''

        # 前进指定步数
        storage['count'] += 1
        if storage['count'] > 2:
            storage['mode'] = 'wander'
            storage['count'] = 2
            return choice('rl1234')

    # 写入模块
    storage['wander'] = wander
    storage['square'] = square
    storage['goback'] = goback

    storage['mode'] = 'wander'
    storage['turn'] = choice('rl')
    storage['count'] = 2
