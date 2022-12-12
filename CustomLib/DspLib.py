# Pypi/Standard Packages
import math
import random
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

###########################################################################
#                           DspLib.py
# Description: This library is a library of useful dsp functions
# Author: Justin Killam
# Last Edited: 12/11/2022
###########################################################################




def FIRResponsePlot(b,fsHz=1,scaleTo='Hz',title='Missing',yLims=[-150,10]):
    """
###########################################################################
                          FIRResponsePlot
Description: Plots the frequency response of FIR filter coefficients
Arguments:
  b : FIR filter coefficients
  fsHz : Sampling frequency in Hz
  scaleTo : SI unit the sampling frequency should be scaled to either
            'Hz','KHz','MHz','GHz'
  title : Title of the figure
  yLims : Y axis limits
Returns:
  Figure object
  Axes objects
###########################################################################
    """
    # Dictionary used for scaling the frquencies for plotting
    scaleDict={
        'GHz':1e9,
        'MHz':1e6,
        'KHz':1e3,
        'Hz':1
    }

    # Scale the sampling frequency according to the selected scale
    fs=(fsHz/scaleDict[scaleTo])

    # Get the frequency response of the filter
    [F,H]=sig.freqz(b,1,1024,fs=fs)

    # Calculate magnitude and phase
    Mag=np.multiply(np.log10(np.absolute(H)),20)
    Phase=np.unwrap(np.angle(H))

    # Plotting
    [Fig,Axs]=plt.subplots(2,1)
    Axs[0].plot(F,Mag)
    Axs[0].set_xlabel('Frequency ('+scaleTo+')')
    Axs[0].set_ylabel('Magnitude (dB)')
    Axs[0].set_ylim(yLims[0],yLims[1])
    Axs[1].plot(F,Phase)
    Axs[1].set_xlabel('Frequency ('+scaleTo+')')
    Axs[1].set_ylabel('Phase (radians)')
    Fig.suptitle(title)

    # Return the figure and axes objects
    return Fig,Axs




def PlotSpectrum(x,fsHz=1,scaleTo='Hz',title='Missing',yLims=[-150,10]):
    """
###########################################################################
                          PlotSpectrum
Description: Plots the spectrum of an input signal
Arguments:
  x : Data for spectral plotting
  fsHz : Sampling frequency in Hz
  scaleTo : SI unit the sampling frequency should be scaled to either
            'Hz','KHz','MHz','GHz'
  title : Title of the figure
  yLims : Y axis limits
Returns:
  Figure object
  Axes objects
###########################################################################
    """

    # Dictionary used for scaling the frquencies for plotting
    scaleDict={
        'GHz':1e9,
        'MHz':1e6,
        'KHz':1e3,
        'Hz':1
    }

    # Scale the sampling frequency according to the selected scale
    fs=(fsHz/scaleDict[scaleTo])

    # Plotting the magnitude and phase spectrum
    [Fig,Axs]=plt.subplots(2,1)
    Axs[0].magnitude_spectrum(x,Fs=fs,sides='twosided',scale='dB')
    Axs[1].phase_spectrum(x,Fs=fs,sides='twosided')
    xtitle=Axs[0].get_xlabel()
    Axs[0].set_xlabel(xtitle+' ('+scaleTo+')')
    Axs[0].set_ylim(yLims[0],yLims[1])
    xtitle=Axs[1].get_xlabel()
    Axs[1].set_xlabel(xtitle+' ('+scaleTo+')')
    Fig.suptitle(title)

    return Fig,Axs




def GenerateBLData(N,fs,fc):
    """
###########################################################################
                          GenerateBLData
Description: Generate band limited random data
Arguments:
  N : Number of data points to be generated
  fs : Sampling frequency in Hz
  fc : Cutoff frequency of data to be generated
Returns:
  Band limited random data
###########################################################################
    """
    
    # Generate Random Data
    random.seed(10)
    data=[]
    for i in range(N):
        data.append(random.random()-0.5)

    #Scale The Data
    data=np.multiply(data,256)

    #Band Limiting Data
    coeffs=sig.firwin(1000,fc,fs=fs)
    data=sig.lfilter(coeffs,1,data)

    return data




def Quantize(x,fracBits):
    """
###########################################################################
                             Quantize
Description: Quantize floating point data to a provided fractional
             precision
Arguments:
  x : Data to be quantized
  fracBits : Fractional precision to quantize to
Returns:
  Quantized data scaled to integer
  Quantized data scaled back to its fixed point value
###########################################################################
    """
    
    scaled= np.multiply(x,2**fracBits)
    integerVal= np.around(scaled)
    fixedVal=np.divide(scaled,2**fracBits)
    return integerVal,fixedVal




def Upsample(x,up):
    """
###########################################################################
                             Upsample
Description: Upsample the input data by zero packing
Arguments:
  x : Data to be upsampled
  up : Ammount of upscaling 
Returns:
  Upsampled data
###########################################################################
    """
    
    outlist=[]
    for val in x:
        outlist.append(val)
        for i in range(up-1):
            outlist.append(0)
    return outlist




def FtoW(freq,fs):
    """
###########################################################################
                             FtoW
Description: Convert a frequncy to the sampled angular frequency
Arguments:
  fs : Data to be upsampled
  freq : Ammount of upscaling 
Returns:
  Sampled angular frequency
###########################################################################
    """
    return (freq/fs)*math.pi*2