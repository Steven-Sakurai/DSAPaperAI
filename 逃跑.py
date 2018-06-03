# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 20:54:10 2018

@author: boyu9
"""
#几处筛选条件存在问题，还需改进
def escape(stat):
    from pythonds.basic.queue import Queue
    
    def escapeDistance(field,band,me,meX,meY,meId,stat):
        if field[meX][meY]==meId:
            return (meX,meY,0)
        searchList=[(meX,meY)]
        searchQueue=Queue()
        if meX-1>=0 and band[meX-1][meY]!=meId:
            searchQueue.enqueue((meX-1,meY,1,2))
            searchList.append((meX-1,meY))
        if meX+1<=100 and band[meX+1][meY]!=meId:
            searchQueue.enqueue((meX+1,meY,1,0))
            searchList.append((meX+1,meY))
        if meY-1>=0 and band[meX][meY-1]!=meId:
            searchQueue.enqueue((meX,meY-1,1,3))
            searchList.append((meX,meY-1))
        if meY+1<=101 and band[meX][meY+1]!=meId:
            searchQueue.enqueue((meX,meY+1,1,1))
            searchList.append((meX,meY+1))
        while True:
            currentPosition=searchQueue.dequeue()
            currentX=currentPosition[0]
            currentY=currentPosition[1]
            currentStep=currentPosition[2]
            direction=currentPosition[3]
            if field[currentX][currentY]==meId:
                return currentPosition
            step=currentStep+1
            for coordinate in [(currentX-1,currentY),(currentX+1,currentY),(currentX,currentY-1),(currentX,currentY+1)]:
                horizon=coordinate[0]
                vertical=coordinate[1]
                if horizon>=0 and horizon<=100 and vertical>=0 and vertical<=101:
                    if field[horizon][vertical]==meId:
                        return (horizon,vertical,step,direction)
                    elif band[horizon][vertical]!=meId and ((horizon,vertical) not in searchList):
                        searchQueue.enqueue((horizon,vertical,step,direction))
                        searchList.append((horizon,vertical))
    
    def murderPossibility(band,enemy,enemyX,enemyY,enemyId,me,meId,distance):
        searchList=[(enemyX,enemyY)]
        searchQueue=Queue()
        searchQueue.enqueue((enemyX,enemyY,0))
        while True:
            currentPosition=searchQueue.dequeue()
            currentX=currentPosition[0]
            currentY=currentPosition[1]
            currentStep=currentPosition[2]    
            if currentStep>=distance+5:
                return False
            step=currentStep+1
            for coordinate in [(currentX-1,currentY),(currentX+1,currentY),(currentX,currentY-1),(currentX,currentY+1)]:
                horizon=coordinate[0]
                vertical=coordinate[1]
                if horizon>=0 and horizon<=100 and vertical>=0 and vertical<=101:
                    if band[horizon][vertical]==meId and step<distance+5:
                        return True
                    elif band[horizon][vertical]!=enemyId and ((horizon,vertical) not in searchList):
                        searchQueue.enqueue((horizon,vertical,step))
                        searchList.append((horizon,vertical))
    
    field=stat['fields']
    band=stat['bands']
    enemy=stat['enemy']
    enemyX=enemy['x']
    enemyY=enemy['y']
    enemyId=enemy['id']
    me=stat['me']
    meId=me['id'] 
    meX=me['x']
    meY=me['y']
    currentDirection=me['direction']
    
    escapeResult=escapeDistance(field,band,me,meX,meY,meId,stat)
    distance=escapeResult[2]
    murder=murderPossibility(band,enemy,enemyX,enemyY,enemyId,me,meId,distance)
    if murder==False:
        return False
    else:
        direction=escapeResult[3]
        symbol=(direction-currentDirection)%4
        if symbol==0:
            return None
        elif symbol==1:
            return 'R'
        elif symbol==3:
            return 'L'
