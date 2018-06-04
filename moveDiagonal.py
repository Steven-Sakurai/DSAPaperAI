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
import numpy as np

def is_move_possible(stat, move):
    '''
    need to judge:
        band
        boundary
        (bunch into enemy?)
    '''
    pos = np.array([stat['now']['me']['x'], stat['now']['me']['y']])
    curDir = stat['now']['me'].direction
    if curDir == 0:
        if move is None:
            pos_next = pos + np.array([1, 0])
        elif move == 'L':
            pos_next = pos + np.array([0, 1])
        elif move == 'R':
            pos_next = pos + np.array([0, -1])
    elif curDir == 1:
        if move is None:
            pos_next = pos + np.array([0, 1])
        elif move == 'L':
            pos_next = pos + np.array([-1, 0])
        elif move == 'R':
            pos_next = pos + np.array([1, 0])
    elif curDir == 2:
        if move is None:
            pos_next = pos + np.array([-1, 0])
        elif move == 'L':
            pos_next = pos + np.array([0, -1])
        elif move == 'R':
            pos_next = pos + np.array([0, 1])
    elif curDir == 3:
        if move is None:
            pos_next = pos + np.array([0, -1])
        elif move == 'L':
            pos_next = pos + np.array([1, 0])
        elif move == 'R':
            pos_next = pos + np.array([-1, 0])
    if (pos_next[0] > stat.size[0]) or (pos_next[1] > stat.size[1]):
        return False
    upperhand = stat['now']['me']['id']
    if stat['now']['band'][pos_next[0]][pos_next[1]] == upperhand:
        return False
    return True

def turn_direction(stat, dest):
    cur = stat['now']['me']['direction']
    if cur - dest == 2 or dest - cur == 2:
        return None
    elif (dest - cur == 1) or (dest - cur == -3):
        return 'L'
    else:
        return 'R'

class ActionL:
    def __init__(self, stat_, moveX_, moveY_):
        self.stat = stat_
        self.moveX = moveX_
        self.moveY_ = moveY_
        self.finished = False 
        self.count = 0
    
    def init(self):    
        destX = 0 if self.moveX >= 0 else 2
        destY = 1 if self.moveY >= 0 else 3 

        xfirst = True
        tmp = turn_direction(self.stat, destX)
        if tmp is None:
            tmp = turn_direction(self.stat, destY)
            xfirst = False 
        
        if xfirst:
            self.moveX -= 1
            if destY - destX == 1:
                self.moves = tmp + [None] * self.moveX + ['L'] + [None] * (self.moveY - 1)
            else:
                self.moves = tmp + [None] * self.moveX + ['R'] + [None] * (self.moveY - 1)
        else:
            self.moveY -= 1
            if destY - destX == 1:
                self.moves = tmp + [None] * self.moveY + ['R'] + [None] * (self.moveX - 1)
            else:
                self.moves = tmp + [None] * self.moveY + ['L'] + [None] * (self.moveX - 1)
        return

    def makeMove(self):
        move = self.moves[count]
        count += 1
        if count > self.moveX + self.moveY:
            self.finished = True
        return move 


# wrapper around ActionL
class ActionDiagonal:
    # risky : 0 ~ ?
    # dir: [+-1, +-1]
    def __init__(self, stat_, risky_, big_direction_, ntimes_):
        self.stat = stat_
        self.risky = risky 
        self.big_direction = big_direction_
        self.ntimes = ntimes_
        self.count = 0

        self.step = 4*risky + 1
        # didn't check illegality here, check it when calling ActionL.makeMove()
        self.home = np.array([stat_['now']['me']['x'], stat_['now']['me']['y']])
        
        if big_direction_ == 0:
            self.direction = np.array([1, 1])
        elif big_direction_ == 1
            self.direction = np.array([-1, 1])
        elif big_direction == 2:
            self.direction = np.array([-1, -1])
        else:
            self.direction = np.array([1, -1])    
    # call this when init, or the previous L is finished
    def init(self):
        self.actionL = ActionL(self.stat, self.direction[0]*(self.risky+1), self.direction[1]*(self.risky+1))
        
    def makeMove(self):
        if self.actionL.finished == False:
            return self.actionL.makeMove()
        else:
            prev_move = self.actionL

            pos = np.array([stat['now']['me']['x'], stat['now']['me']['y']])
            upperhand = stat['now']['me']['id']
            if stat['now']['fields'][pos_next[0]][pos_next[1]] != upperhand:
                self.actionL = ActionL(self.stat, -prev_move.moveX, -prev_move.moveY)
            else:
                self.init()
            self.actionL.init()
            return self.actionL.makeMove()

# need to initialize this
def load(stat, storage):
    storage['Action'] = None

def play(stat, storage):
    move_list = [None, 'L', 'R']
    safe = True # need to implement
    if storage['Action'] is not None:
        action_Now = storage['Action']
    else:
        storage['Action'] = ActionDiagonal(stat, 1, 0, 5)
        action_Now = storage['Action']
        action_Now.init()
    if safe:
        tmp =  action_Now.makeMove()
        if is_move_possible(stat, tmp):
            return tmp 
        else:
            for i in move_list:
                if is_move_possible(stat, i):
                    return i 
    return None


