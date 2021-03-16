class SquareBoard:
    def __init__ (self,owntokens,opponenttokens):
        self.opponenttokens = opponenttokens.copy()
        self.owntokens = owntokens.copy()
        self.movementrecord=[]
    def copy (self):
        opponenttokens=self.opponenttokens.copy()
        owntokens = self.owntokens.copy()
        newboardgame=SquareBoard(owntokens,opponenttokens)
        return newboardgame
def CoorIsValid(coor):
    if (coor[0]>=0 and coor[0]<=7):
        if (coor[1]>=0 and coor[1]<=7):
            return True
    return False
def isEmpty(cor,coor):
    if (cor in coor):
        return False
    else:
        return True
def CoorIsValid(coor):
    if (coor[0]>=0 and coor[0]<=7):
        if (coor[1]>=0 and coor[1]<=7):
            return True
    return False
def getGoalArea(coor):
    goalArea=set()
    for i in coor:
        allgoal=getboomArea(i)
        for tmpgoal in allgoal:
            if(isEmpty(tmpgoal,coor)):
                goalArea.add(tmpgoal)
    return goalArea
def getboomArea(coor):
    x=coor[0]
    y=coor[1]
    result=[]
    ls=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
    for i in ls:
        if(CoorIsValid(i)):
            result.append(i)
    return result
def getBoomResult(boomArea,aimtokens):
    boomtoken=[i for i in aimtokens if i in boomArea]
    if(len(boomtoken)!=0):
        tmptokens=[i for i in aimtokens if i not in boomArea]
        for i in boomtoken:
            boomtoken=boomtoken+getBoomResult(getboomArea(i),tmptokens)
        return boomtoken
    else:
        return []
def getGoal(aimtokens):
    goalArea=getGoalArea(aimtokens)
    result={}
    for point in goalArea:
        boomArea=getboomArea(point)
        result[point]=list(set(getBoomResult(boomArea,aimtokens)))
    return result

def geteva(owntokens,opponenttokens):
    alltokens=owntokens+opponenttokens
    initeva={}
    tmpresult={}
    for i in range(0,8):
        for j in range(0,8):
            point=(i,j)
            boomArea=getboomArea(point)
            tmpresult[point]=list(set(getBoomResult(boomArea,alltokens)))
            evavalue=0
            for coor in tmpresult[point]:
                evavalue+=(opponenttokens.count(coor)-owntokens.count(coor))
            if(isEmpty(point,alltokens) and evavalue!=0):
                if(evavalue<0):
                    evavalue+=1
                else:
                    evavalue-=1
            initeva[point]=evavalue
    return initeva

def getdistance(owntoken,goal,owntokens):
    stack=owntokens.count(owntoken)
    dis1=abs(owntoken[0]-goal[0])
    dis2=abs(owntoken[1]-goal[1])
    if(dis1%stack!=0):
        dis1=(dis1/stack)+1
    else:
        dis1=dis1/stack
    if(dis2%stack!=0):
        dis2=(dis2/stack)+1
    else:
        dis2=dis2/stack
    return dis1+dis2
def gettokengoalcomb(owntokens,opponenttokens):
    initeva=geteva(owntokens,opponenttokens)
    tokengoalcomb=[]
    alltokens=owntokens+opponenttokens
    for goalpoint in initeva.keys():
        if(initeva[goalpoint]>0):
            tmptokens=owntokens
        elif(initeva[goalpoint]<0):
            tmptokens=opponenttokens
        elif(initeva[goalpoint]==0):
            tmptokens=owntokens+opponenttokens
        for tmptoken in tmptokens:
                distance=getdistance(tmptoken,goalpoint,tmptokens)
                #if(initeva[goalpoint]!=0):
                tokengoalcomb.append([goalpoint,tmptoken,distance,initeva[goalpoint]])
    tokengoalcomb=sorted(tokengoalcomb,key=lambda x:(x[2],x[3]))
    return tokengoalcomb


def getchoosentokens(boardgame):
    alltokens=boardgame.opponenttokens+boardgame.owntokens
    tokengoalcomb=gettokengoalcomb(boardgame.owntokens,boardgame.opponenttokens)
    chosentokens=set()
    minvalue=0
    maxvalue=0
    for comb in tokengoalcomb:
        if(tokengoalcomb[0][2]==comb[2]):
            if(comb[3]>=maxvalue):
                maxvalue=comb[3]
            if(comb[3]<minvalue):
                minvalue=comb[3]
        else:
            break
    if(maxvalue>=abs(minvalue)):
        decidevalue=maxvalue
    else:
        decidevalue=minvalue
    for comb in tokengoalcomb:
        if(tokengoalcomb[0][2]==comb[2]):
            if(decidevalue==comb[3]):
                if(decidevalue>=0):
                    chosentokens.add(comb[1])
                else:
                    boomArea=getboomArea(comb[0])
                    tmpresult=list(set(getBoomResult(boomArea,alltokens)))
                    for tmptoken in tmpresult:
                        if tmptoken in boardgame.owntokens:
                            chosentokens.add(tmptoken)
        else:
            break
    '''if(len(chosentokens)==0):
        maxvalue=0
        stepnum=3
        while(len(chosentokens)==0):
            for comb in tokengoalcomb:
                if((comb[3]>=1) and comb[2]<=stepnum):
                    if(comb[3]>=0):
                        chosentokens.add(comb[1])
                    else:
                        boomArea=getboomArea(comb[0])
                        tmpresult=list(set(getBoomResult(boomArea,alltokens)))
                        for tmptoken in tmpresult:
                             if tmptoken in owntokens:
                                 chosentokens.add(tmptoken)
            stepnum+=1'''
    return list(chosentokens)

def updateboomresult(coor,boardgame):
    alltokens=boardgame.owntokens+boardgame.opponenttokens
    tmpowntokens=boardgame.owntokens.copy()
    tmpopponenttokens=boardgame.opponenttokens.copy()
    boomArea=getboomArea(coor)
    result=list(set(getBoomResult(boomArea,alltokens)))
    for owntoken in boardgame.owntokens:
        if(owntoken in result):
            tmpowntokens.remove(owntoken)
    for opponenttoken in boardgame.opponenttokens:
        if(opponenttoken in result):
            tmpopponenttokens.remove(opponenttoken)
    return tmpowntokens,tmpopponenttokens

def makemovementeva(movement):
    boardgame=movement[0]
    owntokens=boardgame.owntokens
    opponenttokens=boardgame.opponenttokens
    #print(owntokens,opponenttokens)
    alltokens=opponenttokens+owntokens
    evavalue=0
    if(movement[1][0]=="BOOM"):
        coor=movement[1][1]
        boomArea=getboomArea(coor)
        tmplist=list(set(getBoomResult(boomArea,alltokens)))
        for coor in tmplist:
            evavalue+=(opponenttokens.count(coor)-owntokens.count(coor))
    else:
        tokengoalcombs=gettokengoalcomb(owntokens,opponenttokens)
        mostvaluable=[]
        mostdan=[]
        for comb in tokengoalcombs:
            if(mostvaluable!=[] and mostdan!=[]):
                break
            if((abs(comb[3])>=1)):
                if(comb[3]>=0):
                    if(mostvaluable==[]):
                        mostvaluable=comb
                else:
                    if(mostdan==[]):
                        mostdan=comb
        if(mostvaluable==[]):
            for comb in tokengoalcombs:
                if(comb[3]==0 and comb[1] in owntokens):
                    mostvaluable=comb
                    break
        if(mostdan==[]):
            for comb in tokengoalcombs:
                if(comb[1] in opponenttokens):
                    mostdan=comb
                    break
        #print(mostvaluable,mostdan)
        tmp1=max(1,mostvaluable[2])
        tmp2=max(1,mostdan[2])
        evavalue=(1.0*mostvaluable[3])/tmp1+(1.0*mostdan[3])/tmp2
    return evavalue





def getinitGoal(owntokens,opponenttokens):
    goaldic=getGoal(opponenttokens)
    initgoals=[]
    for goal in goaldic.keys():
        for owntoken in owntokens:
            distance=abs(owntoken[0]-goal[0])+abs(owntoken[1]-goal[1])
            initgoals.append([goal,owntoken,distance,len(goaldic[goal])])
        

def alphaBeta(white,black,boardgame):
    alpha = 1000
    beta = -1000
    Player = True
    #Make sure depth == maxdepth
    depth = 3
    maxdepth = 3
    #print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")
    print("start\n")
    startmove = (-1,-1)
    # All possible move inside
    #   Movemomen
    possibleMovement = {}
    # The best value
    value = alphaBetaCore(boardgame,depth,alpha,beta,Player,startmove,possibleMovement,white,black,maxdepth)
    print("finish\n")
    print(f"A-B result is {value}")
    print(f"THE MOVEMENT is {possibleMovement}")


def GameOver(owntokens,opponenttokens):
    if(len(owntokens)==0 or len(opponenttokens)==0):
       return True
    return False

def getpossiblemovement(boardgame):
    coors=getchoosentokens(boardgame.copy())
    alltokens=boardgame.owntokens+boardgame.opponenttokens
    result=[]
    directions=[-1,1]
    for point in boardgame.owntokens:
     #boom
        boomArea=getboomArea(point)
        tmplist=list(set(getBoomResult(boomArea,alltokens)))
        if(len([i for i in tmplist if i in boardgame.opponenttokens])!=0):
            newowntokens,newopponenttokens=updateboomresult(point,boardgame.copy())
            newboardgame=SquareBoard(newowntokens,newopponenttokens)
            actiondescribe=("BOOM",point)
            result.append([newboardgame,actiondescribe])
    for coor in coors: 
        stacknumber=boardgame.owntokens.count(coor)
        possiblegoal=[]
        for i in range(1,stacknumber+1):
            for direction in directions:
                    possiblegoal.append((coor[0]+direction*i, coor[1]))
                    possiblegoal.append((coor[0],coor[1]+direction*i))
        possiblegoal= filter(CoorIsValid,possiblegoal)
        possiblegoal=list(possiblegoal)
        tmppossiblegoal=possiblegoal.copy()
        for goal in possiblegoal:
            if goal in boardgame.opponenttokens:
                tmppossiblegoal.remove(goal)
        for goal in tmppossiblegoal:
            owntokens=boardgame.owntokens.copy()
            for i in range(1,stacknumber+1):
                    owntokens.remove(coor)
                    owntokens.append(goal)
                    newboardgame=SquareBoard(owntokens.copy(),boardgame.opponenttokens)
                    tplist=boardgame.movementrecord.copy()
                    actiondescribe=("MOVE",i,coor,goal)
                    tplist.append(actiondescribe)
                    newboardgame.movementrecord=tplist
                    result.append([newboardgame,actiondescribe])

    return result
def alphaBetaCore(movement,depth,alpha,beta,maxdepth,Player):
    #bottom of the tree
    boardgame=movement[0].copy()
    if (GameOver(boardgame.owntokens,boardgame.opponenttokens)):
        #if(Player==True):
        if(len(boardgame.owntokens)==0):
            return (-500,[])
        else:
            return (500,[])
        '''else:
            if(len(boardgame.owntokens)==0):
                print(111)
                return (500,[])
            else:
                return (-500,[])'''
    if (depth==maxdepth):
        tmp=makemovementeva(movement)
        return (makemovementeva(movement),[])
    if(Player==True):
        value=-1000
        choosenmove=[]
        possibleMovements=getpossiblemovement(boardgame)
        #print(possibleMovements)
        for possibleMovement in possibleMovements:
            tmpvalue,tmpls=alphaBetaCore(possibleMovement,depth+1,alpha,beta,maxdepth,False)
            if(tmpvalue>value):
                value=tmpvalue
                choosenmove=possibleMovement[1]
            alpha=max(alpha,value)
            if(beta<=alpha):
                break
        return value,choosenmove
    else:
        value=1000
        newowntokens=movement[0].opponenttokens.copy()
        newopponenttokens=movement[0].owntokens.copy()
        boardgame=SquareBoard(newowntokens,newopponenttokens)
        possibleMovements=getpossiblemovement(boardgame)
        for possibleMovement in possibleMovements:
            #fathermovement.append(possibleMovement[1])
            newowntokens=possibleMovement[0].opponenttokens.copy()
            newopponenttokens=possibleMovement[0].owntokens.copy()
            newboardgame=SquareBoard(newowntokens,newopponenttokens)
            possibleMovement[0]=newboardgame
            tmpvalue,fathermovement=alphaBetaCore(possibleMovement,depth+1,alpha,beta,maxdepth,True)
            value=min(tmpvalue,value)
            beta=min(beta,value)
            if(beta<=alpha):
                break
        return value,boardgame.movementrecord
    '''if(depth!=0):
        newowntokens=movement[0].opponenttokens.copy()
        newopponenttokens=movement[0].owntokens.copy()
        boardgame=SquareBoard(newowntokens,newopponenttokens)
    possibleMovements=getpossiblemovement(boardgame)
    for possibleMovement in possibleMovements:
        fathermovement.append(possibleMovement[1])
        value,fathermovement=alphaBetaCore(possibleMovement,depth+1,-alpha,-beta,maxdepth,fathermovement)
        value=-value
        if(value>=alpha):
            return alpha,fathermovement
        if(value>beta):
            beta=value
    return beta,fathermovement'''

def main():
    owntokens=[(1,0),(1,2)]
    opponenttokens=[(0,0),(0,1)]
    boardgame=SquareBoard(owntokens,opponenttokens)
    movement=[boardgame,[]]
    print(alphaBetaCore(movement,0,-1000,1000,5,True))

if __name__ == '__main__':
    main()

