# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 20:54:10 2018

@author: boyu9
"""
def escape(stat):
    """
    逃跑函数，由三部分构成：
    1.计算当前最短逃跑距离distance （def escapeDistance）
    2.根据最短逃跑距离判断对方在distance+5（此处逃跑阈值可调）步内能否追到 （def murderPossibility）
    3.若能追到，返回按照最短逃跑路径行走一格的指令；若追不到，返回False
    """
    from pythonds.basic.queue import Queue
    
    def escapeDistance(field,band,me,meX,meY,meId,meDirection):
        searchGrid={0:[(1,0,0),(0,-1,3),(0,1,1)],1:[(0,1,1),(1,0,0),(-1,0,2)],2:[(-1,0,2),(0,1,1),(0,-1,3)],3:[(0,-1,3),(1,0,0),(-1,0,2)]}
        if field[meX][meY]==meId:
            return (meX,meY,0,meDirection,meDirection)
        searchList=[(meX,meY)]
        searchQueue=Queue()
        if meX-1>=0 and ((-1,0,2) in searchGrid[meDirection]):
            searchQueue.enqueue((meX-1,meY,1,2,2))
            searchList.append((meX-1,meY))
        if meX+1<=100 and ((1,0,0) in searchGrid[meDirection]):
            searchQueue.enqueue((meX+1,meY,1,0,0))
            searchList.append((meX+1,meY))
        if meY-1>=0 and ((0,-1,3) in searchGrid[meDirection]):
            searchQueue.enqueue((meX,meY-1,1,3,3))
            searchList.append((meX,meY-1))
        if meY+1<=101 and ((0,1,1) in searchGrid[meDirection]):
            searchQueue.enqueue((meX,meY+1,1,1,1))
            searchList.append((meX,meY+1))
        while True:
            currentPosition=searchQueue.dequeue()
            currentX=currentPosition[0]
            currentY=currentPosition[1]
            currentStep=currentPosition[2]
            currentDirection=currentPosition[3]
            historyDirection=currentPosition[4]
            if field[currentX][currentY]==meId:
                return currentPosition
            step=currentStep+1
            for coordinate in searchGrid[currentDirection]:
                horizon=currentX+coordinate[0]
                vertical=currentY+coordinate[1]
                newDirection=coordinate[2]
                if horizon>=0 and horizon<=100 and vertical>=0 and vertical<=101:
                    if field[horizon][vertical]==meId:
                        return (horizon,vertical,step,newDirection,historyDirection)
                    elif band[horizon][vertical]!=meId and ((horizon,vertical) not in searchList):
                        searchQueue.enqueue((horizon,vertical,step,newDirection,historyDirection))
                        searchList.append((horizon,vertical))
    
    def murderPossibility(band,enemy,enemyX,enemyY,enemyId,enemyDirection,me,meId,distance):
        searchGrid={0:[(1,0,0),(0,-1,3),(0,1,1)],1:[(0,1,1),(1,0,0),(-1,0,2)],2:[(-1,0,2),(0,1,1),(0,-1,3)],3:[(0,-1,3),(1,0,0),(-1,0,2)]}
        searchList=[(enemyX,enemyY)]
        searchQueue=Queue()
        searchQueue.enqueue((enemyX,enemyY,0,enemyDirection))
        while True:
            currentPosition=searchQueue.dequeue()
            currentX=currentPosition[0]
            currentY=currentPosition[1]
            currentStep=currentPosition[2]  
            currentDirection=currentPosition[3]
            if currentStep>=distance+5:
                return False
            step=currentStep+1
            for coordinate in searchGrid[currentDirection]:
                horizon=currentX+coordinate[0]
                vertical=currentY+coordinate[1]
                newDirection=coordinate[2]
                if horizon>=0 and horizon<=100 and vertical>=0 and vertical<=101:
                    if band[horizon][vertical]==meId and step<distance+5:
                        return True
                    elif band[horizon][vertical]!=enemyId and ((horizon,vertical) not in searchList):
                        searchQueue.enqueue((horizon,vertical,step,newDirection))
                        searchList.append((horizon,vertical))
    
    field=stat['fields']
    band=stat['bands']
    enemy=stat['enemy']
    enemyX=enemy['x']
    enemyY=enemy['y']
    enemyId=enemy['id']
    enemyDirection=enemy['direction']
    me=stat['me']
    meId=me['id'] 
    meX=me['x']
    meY=me['y']
    meDirection=me['direction']
    
    escapeResult=escapeDistance(field,band,me,meX,meY,meId,meDirection)
    distance=escapeResult[2]
    murder=murderPossibility(band,enemy,enemyX,enemyY,enemyId,enemyDirection,me,meId,distance)
    if murder==False:
        return False
    else:
        targetDirection=escapeResult[-1]
        symbol=(targetDirection-meDirection)%4
        if symbol==0:
            return None
        elif symbol==1:
            return 'R'
        elif symbol==3:
            return 'L'
