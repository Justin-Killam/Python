import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
import random

# b       : zero coeficients of the fir
# fsHz    : sampling frequency in Hz
# scaleTo : what the fs should be scaled to for plots either
#               'Hz','KHz','MHz','GHz'
# Title   : Title of the figure
def FIRResponsePlot(b,fsHz=1,scaleTo='Hz',Title='Missing'):
    scaleDict={
        'GHz':1e9,
        'MHz':1e6,
        'KHz':1e3,
        'Hz':1
    }
    fs=(fsHz/scaleDict[scaleTo])

    [F,H]=sig.freqz(b,1,1024,fs=fs)
    Mag=np.multiply(np.log10(np.absolute(H)),20)
    Phase=np.unwrap(np.angle(H))
    
    [Fig,Axs]=plt.subplots(2,1)
    Axs[0].plot(F,Mag)
    Axs[0].set_xlabel('Frequency ('+scaleTo+')')
    Axs[0].set_ylabel('Magnitude (dB)')
    Axs[1].plot(F,Phase)
    Axs[1].set_xlabel('Frequency ('+scaleTo+')')
    Axs[1].set_ylabel('Phase (radians)')
    
    Fig.suptitle(Title)
    return [Fig,Axs]
    
# x       : data to plot the responses for
# fsHz    : sampling frequency in Hz
# scaleTo : what the fs should be scaled to for plots either
#               'Hz','KHz','MHz','GHz'
# Title   : Title of the figure
def PlotSpectrum(x,fsHz=1,scaleTo='Hz',Title='Missing'):
    scaleDict={
        'GHz':1e9,
        'MHz':1e6,
        'KHz':1e3,
        'Hz':1
    }
    fs=(fsHz/scaleDict[scaleTo])

    [Fig,Axs]=plt.subplots(2,1)
    Axs[0].magnitude_spectrum(x,Fs=fs,sides='twosided',scale='dB')
    Axs[1].phase_spectrum(x,Fs=fs,sides='twosided')
    
    xtitle=Axs[0].get_xlabel()
    Axs[0].set_xlabel(xtitle+' ('+scaleTo+')')
    xtitle=Axs[1].get_xlabel()
    Axs[1].set_xlabel(xtitle+' ('+scaleTo+')')
    
    Fig.suptitle(Title)
    
    return [Fig,Axs]
    
# Generate N data points of noise data band limited to 
# fc in hertz with fs in hertz as a reference
def GenerateBLData(N,fs,fc):
    random.seed(10)
    data=[]
    for i in range(N):
        data.append(random.random()-0.5)
    data=np.multiply(data,256)

    #Band Limiting Data
    coeffs=sig.firwin(1000,fc,fs=fs)
    data=sig.lfilter(coeffs,1,data)
    
    return data