# Pypi/Standard Packages
import math
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

# Custom Packages
from CustomLib.DspLib import *
from CustomLib import PolyphaseResampler as pprs

# Function for generating test data so data can be change
# without changing code body
def GenerateTestData(points,StartFS,SigF,StartW,bw):
    data=[]
    for i in range(points):
        data.append(math.cos(i*StartW))
    # data=GenerateBLData(points,StartFS,SigF)
    intData,fixedData=Quantize(data,bw)
    return fixedData
    
###########################################################################
#                      Configuration Variables
###########################################################################

#Filter Configuration
up=32
down=33
multipliers=8
filtTaps=multipliers*up
#Ensuring Odd Number of Coefficients
if(filtTaps%2==0):
    filtTaps=filtTaps-1

#Data and Frequency Variables
TestPoints=int(1E5)
StartFS=30E6
SigF=1E6
StartW=FtoW(SigF,StartFS)
FilterF=1.3*SigF

#Calculating Post Resample Frequencies
PostUpFS=StartFS*up
NewFS=PostUpFS/down

#Filter Corner Frequency
FilterWc=FtoW(FilterF,PostUpFS)

PlotLimits=[-150,10]

coeffFrac=15
inFrac=15
outFrac=16
###########################################################################


###########################################################################
#                      Empty Lists
###########################################################################
FigureList=[]
AxesList=[]
###########################################################################

###########################################################################
#                      Main Test
###########################################################################

# Test Signal Generation
TestSignal=GenerateTestData(TestPoints,StartFS,SigF,StartW,inFrac) 

#Creating Resampler Object
resampler=pprs.PolyphaseResampler(up,down,multipliers,filtTaps,FilterWc)
coeffs=resampler.GetFilterCoeffs()
intCoeffs,newCoeffs=Quantize(coeffs,coeffFrac)
resampler.ManualFilterCoeffs(newCoeffs)

#Resampler
OutSignal=[]
for val in TestSignal:
    retVals=resampler.ProcessNewSample(val)
    for outval in retVals:
        OutSignal.append(outval)
intOut,OutSignal=Quantize(OutSignal,outFrac)

###########################################################################
#                      Plotting
###########################################################################

## Plotting Test Signal
[fig,axes]=PlotSpectrum(TestSignal,fsHz=StartFS,scaleTo='MHz',title='Starting Spectrum',yLims=PlotLimits)
FigureList.append(fig)
AxesList.append(axes)

##Plotting a unfiltered zero packed upsampled input signal for visualization
[fig,axes]=PlotSpectrum(Upsample(TestSignal,up),fsHz=StartFS*up,scaleTo='MHz',title='Input Signal Zero Packed Spectrum',yLims=PlotLimits)
FigureList.append(fig)
AxesList.append(axes)

##Plotting the frequency response of the polyphase filter
[fig,axes]=FIRResponsePlot(resampler.GetFilterCoeffs(),fsHz=StartFS*up,scaleTo='MHz',title='Resampler Filter Response',yLims=PlotLimits)
FigureList.append(fig)
AxesList.append(axes)

##Plot spectrun of output signal
[fig,axes]=PlotSpectrum(OutSignal,fsHz=NewFS,scaleTo='MHz',title='Output Spectrum',yLims=PlotLimits)
FigureList.append(fig)
AxesList.append(axes)

plt.show()