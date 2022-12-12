import matplotlib.pyplot as plt

up=32
down=15

points=10000
n=[]
upSamps=[]
downSamps=[]
for i in range(points):
    n.append(i)
    if((i%up)==0):
        upSamps.append(1)
    else:
        upSamps.append(0)
    if((i%down)==0):
        if(i%up==0):
            downSamps.append(up)
        else:
            downSamps.append(i%up)
    else:
        downSamps.append(0)
fig1,axes1=plt.subplots(2,1)
axes1[0].stem(n,upSamps)
axes1[1].stem(n,downSamps)

outEn=[]
outPhase=[]
curPhase=0
for i in range(points):
    if(up<down):
        if((i%up)==0):
            if(curPhase<up):
                outEn.append(1)
                outPhase.append(curPhase)
                curPhase+=down-up
            else:
                outEn.append(0)
                outPhase.append(0)
                curPhase-=up
        else:
            outEn.append(0)
            outPhase.append(0)
    if(up>down):
        if((i%up)==0):
            if(curPhase>=up):
                curPhase-=up 
            outEn.append(1)
            outPhase.append(curPhase)
            curPhase+=down 
        elif(curPhase<up):
            outEn.append(1)
            outPhase.append(curPhase)
            curPhase+=down 
        else:
            outEn.append(0)
            outPhase.append(0)
            
fig2,axes2=plt.subplots(2,1)
axes2[0].stem(n,outEn)
axes2[1].stem(n,outPhase)

plt.show()