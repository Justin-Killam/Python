import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from CustomLib.DspLib import *

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
            if(start==1 or Cnt>down-up):
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


#Test Parameters

points=3000
fs=100e6
fc=3e6
upPoints=[1,3,8]
dnPoints=[1,3,8]



test_vals=GenerateBLData(points,fs,fc)
FigList=[]
AxsList=[]
[Fig,Axs]=PlotSpectrum(test_vals,fsHz=fs,scaleTo='MHz',Title="Starting Spectrum")
FigList.append(Fig)
AxsList.append(Axs)

for up in upPoints:
    for down in dnPoints:
        RetList=FractionalResampler(test_vals,up,down)
        
        ExpRatio=(up)/(down)
        ActRatio=len(RetList)/points
        
        NewFS=fs*ActRatio
        b=sig.firwin(32,fc*1.3,fs=NewFS)
        FilteredData=sig.lfilter(b,1,RetList)
        
        print("Up: "+str(up)+ " Down: "+str(down)+" Expected Ratio: "+str(ExpRatio)+" Actual Ratio : " +str(ActRatio))
        [Fig,Axs]=PlotSpectrum(RetList,fsHz=NewFS,scaleTo='MHz',Title="Up:"+str(up)+" Down:"+str(down)+" Spectrum")
        FigList.append(Fig)
        AxsList.append(Axs)
        
        [Fig,Axs]=PlotSpectrum(FilteredData,fsHz=NewFS,scaleTo='MHz',Title="Up:"+str(up)+" Down:"+str(down)+"Filtered Spectrum")
        FigList.append(Fig)
        AxsList.append(Axs)
        
plt.show()        
