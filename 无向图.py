#判断无向图是否同构
#对于图G1=<V1,E1>，图G2=<V2,E2>
#找到一个从V1到V2的双射函数，把V1通过这个函数全换成V2，使得新的G1=G2。即可证明同构。
#图的表示，点的列表，边利用集合表示，（key,value[i]）表示在key和value[i]之间存在一条无向边
#V1=[vex1,vex2,vex3,...]
#G1={vex1:[vex11,vex12,...],vex2:[vex1,vex2,...],...}

from itertools import permutations
#获取图的输入
def getUndigraph():
    vexlist=list(input().split())#输入节点名称，空格分开
    edgelist=list(input().split())#输入边，格式为(vex1,vex2)，空格分开
    edgedict={}
    for x in edgelist:#存在(a,b)必然存在(b,a)
        x=list(x.split(","))
        x=[x[0][1:],x[1][:-1]]
        if x[0] in edgedict:
            edgedict[x[0]].append(x[1])
        else:
            edgedict[x[0]]=[x[1]]
        if x[1] in edgedict:
            edgedict[x[1]].append(x[0])
        else:
            edgedict[x[1]]=[x[0]]
    return vexlist,edgedict

#返回值deg1={0:[vexlist],1:[vexlist],...}
def classifyByDeg(v1:list,e1:dict):
    d1={x:[] for x in range(max([len(x) for x in e1.values()])+1)}
    for x in v1:
        if x in e1:
            d1[len(e1[x])].append(x)
        else:
            d1[0].append(x)
    return d1

#利用图同构的必要条件判断是否不同构。节点数目相同；边数相同；度数相同的节点数相同
def apprentlyNot(deg1:dict,deg2:dict):
    if sum([len(x) for x in deg1.values()])!=sum([len(x) for x in deg2.values()]):
        print("你这图有问题啊，点数对不上")
        exit()
    
    if sum([x*len(deg1[x]) for x in deg1.keys()])!=sum([x*len(deg2[x]) for x in deg2.keys()]):
        print("你这图有问题啊，边数对不上")
        exit()
    
    if {x:len(deg1[x]) for x in deg1.keys()}!={x:len(deg2[x]) for x in deg2.keys()}:
        print("你这图有问题啊，度数对不上")
        exit()

#对应度数之间产生一一对应，再组合起来，成为可能的双射
def makeBijection(deg1:dict,deg2:dict):
    comblist=[[] for i in range(len(deg1))]
    for i in range(len(deg1)):
        for y in permutations(deg1[i]):
            combdict={}
            for x in zip(y,deg2[i]):
                combdict[x[0]]=x[1]
            comblist[i].append(combdict)
    while(len(comblist)>=2):
        newlist=[dict(x,**y) for x in comblist[0] for y in comblist[1]]
        comblist=[newlist]+comblist[2:]
    return comblist[0]

#判断是否同构
def judge(f,e1:dict,e2:dict):
    for x in f:
        a=sorted([f[old] for old in e1[x]])
        b=sorted(e2[f[x]])
        if a!=b:
            return 0
    else:
        return 1



vex1,edge1=getUndigraph()
vex2,edge2=getUndigraph()
deg1,deg2=classifyByDeg(vex1,edge1),classifyByDeg(vex2,edge2)
apprentlyNot(deg1,deg2)
bijection=makeBijection(deg1,deg2)
for x in bijection:
    if judge(x,edge1,edge2):
        print("好耶，是同构的")
        print(", ".join([old+'->'+x[old] for old in x.keys()]))
        break
else:
    print("不同构")