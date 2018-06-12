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
    from datetime import datetime
    directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    dirs = ['l', 'r']
    left = np.array([[0, 1], [-1, 0]])
    right = np.array([[0, -1], [1, 0]])

    size, field, band, me = stat['size'], stat['now']['fields'], stat['now']['bands'], stat['now']['me']
    storage['myOrder'] = me['id'] # 1, 2
    storage['n'] = 0
    #myField: 0: nothing, 1: my field, 2: my band, 3: his field, 4: his band
    # 41: my_field and his_band,  23: his_field and my band
    if 'ngame' not in storage:
        storage['ngame'] = 0
        storage['win'] = np.repeat(-1, 20)
        storage['dist_escape'] = np.repeat(15, 20)
        storage['risky'] = 0.1

    def update(stat, storage):
        myOrder = storage['myOrder']
        # 开场速攻
        storage['n'] += 1
        if storage['n'] <= 3:
            storage['conserv'] = 3
        elif storage['n'] <= 8:
            storage['conserv'] = 4
        else:
            storage['conserv'] = 5
        # update myField
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
                    myField[i, j] = myField[i, j] * 10 + 1
                else:
                    myField[i, j] = myField[i, j] * 10 + 3
        storage['myField'] = myField

        # update position
        enemy_pos = np.array([stat['now']['enemy']['x'], stat['now']['enemy']['y']])
        my_pos = np.array([stat['now']['me']['x'], stat['now']['me']['y']])
        enemy_fields = np.r_[np.c_[np.where(myField == 3)], np.c_[np.where(myField == 23)]]
        enemy_bands = np.r_[np.c_[np.where(myField == 4)], np.c_[np.where(myField == 41)]]
        storage['my_pos'] = my_pos
        storage['enemy_pos'] = enemy_pos
        storage['enemy_fields'] = enemy_fields
        storage['enemy_bands'] = enemy_bands

        # update cur score
        storage['enemy_score'] = np.c_[np.where(myField % 10 == 3)].shape[0] + 1
        storage['my_score'] = np.c_[np.where(myField % 10 == 1)].shape[0] + 1

        # others
        storage['enemy'] = stat['now']['enemy']

        # update prefered direction
        dir_now = directions[me['direction']]
        dist_now = np.sum(np.abs(my_pos - enemy_pos))

        dist_next = np.zeros([2, 1])
        dist_fields_next = np.zeros([2, 1])
        blank_pos = np.c_[np.where(myField == 0)]
        dist_blank_next = np.zeros([2, 1])
        for d in dirs:
            if d == 'l':
                dir_next = np.matmul(left, dir_now)
                my_pos_tmp = my_pos + dir_next
                dist_next[0] = np.sum(np.abs(my_pos_tmp - enemy_pos))
                dist_fields_next[0] = np.mean(np.abs(enemy_fields - my_pos_tmp))
                dist_blank_next[0] = np.mean(np.abs(my_pos_tmp - blank_pos))
            elif d == 'r':
                dir_next = np.matmul(right, dir_now)
                my_pos_tmp = my_pos + dir_next
                dist_next[1] = np.sum(np.abs(my_pos_tmp - enemy_pos))
                dist_fields_next[1] = np.mean(np.abs(enemy_fields - my_pos_tmp))
                dist_blank_next[1] = np.mean(np.abs(my_pos_tmp - blank_pos))

        if dist_next[0] <= dist_next[1]:
            prefered_dir = 0
        else:
            prefered_dir = 1

            # 开场追打
            if storage['n'] <= 40:
                if dist_next[0] <= dist_next[1]:
                    prefered_dir = 0
                else:
                    prefered_dir = 1
            else:
                # 敌人出窝，追着打
                if storage['enemy_bands'].shape[0] > 1:
                    if dist_next[0] < dist_next[1]:
                        prefered_dir = 0
                    else:
                        prefered_dir = 1

            # # 如果赢着，就避开敌人
            # if storage['my_score'] > storage['enemy_score'] and storage['my_score'] > (1+storage['risky'])*2000:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 1
            #     else:
            #         prefered_dir = 0
            # elif dist_now < storage['dist_escape'][storage['ngame']]:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 1
            #     else:
            #         prefered_dir = 0
            # if storage['my_score'] <= (1+storage['risky'])*storage['enemy_score']:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 0
            #     else:
            #         prefered_dir = 1

            # # 如果敌人在我地盘里，就追他
            # if myField[enemy_pos[0], enemy_pos[1]] % 10 == 1:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 0
            #     else:
            #         prefered_dir = 1

            # # 如果以上均不是
            # if prefered_dir is None:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 0
            #     else:
            #         prefered_dir = 1

            # if myField[enemy_pos[0], enemy_pos[1]] % 10 == 1:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 1
            #     else:
            #         prefered_dir = 0

            # if storage['my_score'] > 1000 + storage['enemy_score'] and dist_now < storage['dist_escape'][storage['ngame']]:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 1
            #     else:
            #         prefered_dir = 0
            # else:
            #     if dist_next[0] < dist_next[1]:
            #         prefered_dir = 0
            #     else:
            #         prefered_dir = 1
        # update prefered_dir over
        storage['prefered_dir'] = prefered_dir
        return

    storage['Update'] = update
    update(stat, storage)
    myField = storage['myField']
    my_pos = storage['my_pos']
    enemy_pos = storage['enemy_pos']

    # 计算安全距离
    def dist(me, enemy, conserv=5):
        return max(2, (abs(enemy['x'] - me['x']) + abs(enemy['y'] - me['y']))//conserv)

    def ifkill():
        class node:
            def __init__(self, dir, pos):
                self.dire = dir  # with the type same with dir_now, which is a np.array
                self.pos = pos

        class binode:
            def __init__(self, idenme, idenen, round, band, prev=None, value=0):  # iden: class node
                self.me = idenme
                self.enemy = idenen
                self.round = round
                self.band = band
                self.value = value
                self.prev = prev
                self.left = None
                self.none = None
                self.right = None

        class tree:
            def __init__(self, root, depth):  # root is binode type
                self.root = root
                self.depth = depth
                if self.depth > 0:
                    if root.round == "me":
                        next = self.root.me.pos + np.matmul(left, self.root.me.dire)
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 21 != 2:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 7 + 2
                            newme = node(next - self.root.me.pos, next)
                            self.root.left = tree(
                                binode(newme, self.root.enemy, "enemy", self.root.band + deltaband, self.root),
                                depth - 1)
                            if owner % 39 == 4:
                                self.root.left.root.value = 1
                        next = self.root.me.pos + self.root.me.dire
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 21 != 2:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 7 + 2
                            newme = node(self.root.me.dire, next)
                            self.root.none = tree(
                                binode(newme, self.root.enemy, "enemy", self.root.band + deltaband, self.root),
                                depth - 1)
                            if owner % 39 == 4:
                                self.root.none.root.value = 1
                        next = self.root.me.pos + np.matmul(right, self.root.me.dire)
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 21 != 2:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 7 + 2
                            newme = node(next - self.root.me.pos, next)
                            self.root.right = tree(
                                binode(newme, self.root.enemy, "enemy", self.root.band + deltaband, self.root),
                                depth - 1)
                            if owner % 39 == 4:
                                self.root.right.root.value = 1
                    else:
                        next = self.root.enemy.pos + np.matmul(left, self.root.enemy.dire)
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 39 != 4:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 39 + 4
                            newen = node(next - self.root.enemy.pos, next)
                            self.root.left = tree(
                                binode(self.root.enemy, newen, "me", self.root.band + deltaband, self.root), depth - 1)
                            if owner % 21 == 2:
                                self.root.left.root.value = -1
                        next = root.enemy.pos + root.me.dire
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 39 != 4:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 39 + 4
                            newen = node(self.root.enemy.dire, next)
                            self.root.none = tree(
                                binode(self.root.enemy, newen, "me", self.root.band + deltaband, self.root), depth - 1)
                            if owner % 21 == 2:
                                self.root.none.root.value = -1
                        next = root.enemy.pos + np.matmul(right, root.enemy.dire)
                        owner = self.root.band[next[0], next[1]]
                        if np.sum(next > 0) == 2 and next[0] < size[0] and next[1] < size[1] and owner % 39 != 4:
                            deltaband = np.zeros((size[0], size[1]))
                            deltaband[next[0], next[1]] += owner * 39 + 4
                            newen = node(next - self.root.enemy.pos, next)
                            self.root.right = tree(
                                binode(self.root.enemy, newen, "me", self.root.band + deltaband, self.root), depth - 1)
                            if owner % 21 == 2:
                                self.root.right.root.value = -1

            def setvalue(self):
                subtree = []
                if self.root.left is not None:
                    subtree.append(self.root.left)
                if self.root.none is not None:
                    subtree.append(self.root.none)
                if self.root.right is not None:
                    subtree.append(self.root.right)
                if len(subtree)>0:
                    if self.root.round == "me":
                        self.root.value = min([x.setvalue() for x in subtree])
                    else:
                        self.root.value = max([x.setvalue() for x in subtree])
                return self.root.value
        print(datetime.now())
        mynode = node(directions[me['direction']], my_pos)
        print(datetime.now())
        enemynode = node(directions[stat['now']['enemy']['direction']], enemy_pos)
        print(datetime.now())
        judgetree = tree(binode(mynode, enemynode, "me", myField), 8)
        print(datetime.now())
        return judgetree.setvalue(), judgetree

    def kill(field, me, storage):
        if storage['tree'].root.left.value == 1:
            storage['tree'] = storage['tree'].root.left
            return 'l'
        elif storage['tree'].root.none.value == 1:
            storage['tree'] = storage['tree'].root.none
            return None
        else:
            storage['tree'] = storage['tree'].root.right
            return 'r'

    def wander(field, me, storage):
        myField = storage['myField']
        if np.sum(np.abs(storage['my_pos'] - storage['enemy_pos'])) < 8 and myField[storage['enemy_pos'][0], storage['enemy_pos'][1]] != 3:
            result = ifkill()
            if result[0] == 1:
                storage['mode'] = "kill"
                storage['tree'] = result[1]
                storage['mode']= "kill"
                return kill(field, me, storage)
        
        # 防止出界
        # x轴不出界
        nextx = me['x'] + directions[me['direction'], 0]
        if nextx <= 1 and me['direction'] != 0 or nextx >= len(
                field) - 2 and me['direction'] != 2:
            storage['mode'] = 'goback'
            storage['count'] = 0
            if me['direction'] % 2 == 0:  # 掉头
                next_turn = dirs[storage['prefered_dir']]
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
                next_turn = dirs[storage['prefered_dir']]
                storage['turn'] = next_turn
                return next_turn
            else:
                return 'lr' [(nexty <= 1) ^ (me['direction'] == 2)]

        # 状态转换
        if field[me['x']][me['y']] != me['id']:
            storage['mode'] = 'square'
            storage['count'] = randrange(1, 3)
            storage['turn'] = dirs[storage['prefered_dir']]
            storage['maxl'] = dist(me, storage['enemy'])
            return ''

        # 随机前进，转向频率递减
        if randrange(storage['count']) == 0:
            storage['count'] += 3
            return dirs[storage['prefered_dir']]

    # 领地外画圈
    def square(field, me, storage):
        if np.sum(np.abs(storage['my_pos'] - storage['enemy_pos'])) < 8 and myField[storage['enemy_pos'][0], storage['enemy_pos'][1]] != 3:
            result = ifkill()
            if result[0] == 1:
                storage['mode'] = "kill"
                storage['tree'] = result[1]
                storage['mode']= "kill"
                return kill(field, me, storage)


        enemy = storage['enemy']
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

            enemy_field = np.c_[np.where(myField % 10 == 3)]
            min_dis = 10000
            for ep in enemy_field:
                thedis = np.sum(np.abs(ep - my_pos))
                if thedis < min_dis:
                    min_dis = thedis
            if hisDist < 10:
                storage['conserv'] = 6
            elif min_dis < hisDist / 4:
                storage['conserv'] = 4

            storage['maxl'] = dist(me, storage['enemy'], storage['conserv'])
            storage['turn'] = dirs[storage['prefered_dir']]
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
    storage['kill'] = kill

    storage['mode'] = 'wander'
    storage['turn'] = dirs[storage['prefered_dir']]
    storage['count'] = 2

def summary(match_result, stat, storage):
    '''
    if I win, I set the following games' parameter as the current one
    If I'm killed, I increase my conservation
    If I lost by score, I decrease my conservation
    '''
    myOrder = storage['myOrder']
    storage['ngame'] += 1
    last_dist = storage['dist_escape'][storage['ngame'] - 1]

    win = myOrder == (match_result[0]+1)
    storage['win'][storage['ngame'] - 1] = win

    if win:
        storage['dist_escape'][storage['ngame']:] = last_dist
    elif not win and match_result[1] != 3:
        storage['win'][storage['ngame'] - 1] = -99
        storage['dist_escape'][storage['ngame']] = last_dist + 3
    elif not win and last_dist > 10:
        storage['dist_escape'][storage['ngame']] = last_dist - 2

# to-do: construct a tree and update the status of the whole field; judge the condition each time