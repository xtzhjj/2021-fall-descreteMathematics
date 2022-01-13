from GameMap import GameMap

def dead(x):
    return x+int(-x**0.5)    
    
class player_class: 
    def __init__(self, player_id:int):
        self.player_id = player_id
        self.depdic={}
        self.time=0
        self.process='initial'

    def player_func(self, map_info):
        return self.myaction(map_info, self.player_id)
    
    def getdepth(self,map_info,player_id):
        nodesList=map_info.nodes
        if player_id==0:
            startNode=nodesList[map_info.N]
        else:
            startNode=nodesList[1]
        vertList=[]
        self.depdic[startNode.number]=0
        vertList.insert(0,startNode)
        while vertList:
            currentVert=vertList.pop()
            for nbr in currentVert.get_next():
                if nbr not in self.depdic:
                    self.depdic[nbr]=self.depdic[currentVert.number]+1
                    vertList.insert(0,nodesList[nbr])
    
    def myaction(self,map_info,player_id):
        nodesList=map_info.nodes
        actionsList=[]
        if not self.depdic:
            self.getdepth(map_info,player_id)          
        occupied=sorted([x.number for x in nodesList if x.belong==player_id],key=lambda x:self.depdic[x],reverse=True)
        dodic={} 
        for nbr in occupied:
            #这里需要根据游戏阶段process:int和编号为nbr:int节点内的实际兵力数nodesList[nbr].power[player_id]:float和节点的总兵力数dodic[nbr]:float确定派出的兵力数powertosend:float
            #注意维护dodic:dict
            #code here:
            if nbr not in dodic:
                dodic[nbr]=nodesList[nbr].power[player_id]
#             if self.process=='initial' and self.time<7:
#                 powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-9)
#                 if powertosend<=1:
#                     continue
#                 else:
#                     dodic[nbr]-=powertosend
#             elif self.process=='initial':
#                 powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-16)
#                 if powertosend<=1:
#                     continue
#                 else:
#                     dodic[nbr]-=powertosend                
#             else:
#                 powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-48)
#                 if powertosend<=1:
#                     continue
#                 else:
#                     dodic[nbr]-=powertosend
            #这里需要通过nodesList[nbr].get_next():list获得编号为nbr:int的节点的所有邻接节点的编号组成的initpossibletargetList:list
            #注意维护dodic:dict
            #code here:
            initpossibletargetList=nodesList[nbr].get_next()
            for nbr0 in initpossibletargetList:
                if nbr0 not in dodic:
                    if nodesList[nbr0].belong==player_id:
                        dodic[nbr0]=nodesList[nbr0].power[player_id]
                    elif nodesList[nbr0].belong==1-player_id:
                        dodic[nbr0]=0-nodesList[nbr0].power[1-player_id]
                    else:
                        dodic[nbr0]=0
            #这里需要将initpossibletargetList中的编号以abs(dodic[x]):float为关键字由小到大排序
            #code here:
            initpossibletargetList=sorted(initpossibletargetList,key=lambda x:dodic[x])
            initpossibletargetList1=sorted(initpossibletargetList,key=lambda x:abs(dodic[x]))
            if dodic[initpossibletargetList1[0]]==0:
                #这里需要一个当邻接节点中有空白节点时的派兵方案
                #已知：powertosend:int initpossibletargetList1:list
                #直接维护actionsList:list(tuple)
                #注意维护dodic:dict
                #code here:
                powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-4.1)
                targetList=sorted([x for x in initpossibletargetList if dodic[x]==0],reverse=True)
                if powertosend/len(targetList)>=3:
                    for x in targetList:                      
                        actionsList.append((nbr,x,powertosend/len(targetList)))
                        dodic[x]=dead(powertosend/len(targetList))
                else:
                    for x in targetList:
                        if powertosend<1:
                            break
                        else:
                            if powertosend<3:
                                actionsList.append((nbr,x,powertosend))
                                dodic[x]=dead(powertosend)
                                break
                            else:
                                actionsList.append((nbr,x,3))
                                powertosend-=3
                                dodic[x]=dead(3)
            else:
                if self.process=='initial' and self.time<5:
                    powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-8)
                    if powertosend<=1:
                        continue
                    else:
                        dodic[nbr]-=powertosend                    
                elif self.process=='initial' and self.time<7:
                    powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-15.2)
                    if powertosend<=1:
                        continue
                    else:
                        dodic[nbr]-=powertosend
                elif self.process=='initial':
                    powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-28)
                    if powertosend<=1:
                        continue
                    else:
                        dodic[nbr]-=powertosend                
                else:
                    powertosend=min(nodesList[nbr].power[player_id]-0.1,dodic[nbr]-48)
                    if powertosend<=1:
                        continue
                    else:
                        dodic[nbr]-=powertosend      
                #这里需要将initpossibletargetList中的编号以dodic[x]:float为关键字由小到大排序
                #code here:
                initpossibletargetList2=sorted(initpossibletargetList,key=lambda x:dodic[x])
                if dodic[initpossibletargetList2[0]]<0:
                    self.process='final'
                    targetList=sorted([x for x in initpossibletargetList2 if dodic[x]<0],key=lambda x:abs(dodic[x])/len([a for a in nodesList[x].get_next() if nodesList[a].belong==player_id]))
                    mytarget=targetList[0]
                    mynodes=len([a for a in nodesList[mytarget].get_next() if nodesList[a].belong==player_id])
                    if dead(powertosend)*0.75*mynodes<abs(dodic[mytarget]):
                        self.depdic[nbr]-=2
                        continue
                    else:
                        actionsList.append((nbr,mytarget,powertosend))
                        dodic[mytarget]-=dead(powertosend)
                    #这里需要一个当邻接节点中有敌方节点时的派兵方案
                    #已知：powertosend:int initpossibletargetList2:list dodic:dict
                    #直接维护actionsList:list(tuple)
                    #注意维护dodic:dict
                    #code here
#                     if dead(powertosend)>=abs(self.dodic[targetList[0]])+0.01:
                    
#                     else:
#                         actionsList.append((nbr,targetList[0],powertosend))
#                         dodic[targetList[0]]-=dead(powertosend)
                else:
                    #这里需要将initpossibletargetList中的编号以self.depdic[x]:int为关键字由大到小排序
                    #code here
                    initpossibletargetList3=sorted(initpossibletargetList,key=lambda x:self.depdic[x])
                    #这里需要一个当邻接节点中只有己方节点时的派兵方案
                    #已知：powertosend:int initpossibletargetList3:list dodic:dict
                    #直接维护actionsList:list(tuple)
                    #注意维护dodic:dict
                    if self.depdic[initpossibletargetList3[0]]>=self.depdic[nbr]:
                        self.depdic[nbr]=self.depdic[initpossibletargetList3[0]]+1
                    actionsList.append((nbr,initpossibletargetList3[0],powertosend))
                    dodic[initpossibletargetList3[0]]+=dead(powertosend)
        self.time+=1
        return actionsList
     
    '''这玩意的配套文件找不到了。。。
