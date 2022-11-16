import numpy as np

def FractionalResampler(x,up,down):
    tempList=[]

    if(up>down):
        Cnt=0
        for val in x:
            tempList.append(val)
            Cnt=Cnt+down
            while(Cnt<up):
                tempList.append(0)
                Cnt=Cnt+down
            Cnt=Cnt-up
        return tempList
    elif(down>up):
        Cnt=0
        start=1
        for val in x:
            if(start==1 or Cnt+up>down):
                tempList.append(val)
                if(start==1):
                    start=0
                    Cnt=Cnt+up
                else:
                    Cnt=Cnt+up-down
            else:
                Cnt=Cnt+up         
        return tempList
    else:
        return x


points=100
test_vals=[]
for i in range(points):
    test_vals.append(i)
vecLen=len(test_vals)

for i in range(8):
    for j in range(8):
        RetList=FractionalResampler(test_vals,i+1,j+1)
        ExpRatio=(i+1)/(j+1)
        ActRatio=len(RetList)/vecLen
        print("Up: "+str(i+1)+ " Down: "+str(j+1)+" Expected Ratio: "+str(ExpRatio)+" Actual Ratio : " +str(ActRatio))
        print(RetList)    
