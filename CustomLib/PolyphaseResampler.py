# Pypi/Standard Packages
import math
import scipy.signal as sig


class PolyphaseResampler:
    """
###########################################################################
                        PolyphaseResampler
Description: Polyphase resampler object for arbitrary resampling
             and interpolation using a polyphase filter
Arguments:
  up : Upsample amount
  down : Downsample amount
  mults : Number of multiplications allowed
  filtTaps : Number if filter taps to use in the polyphase filter
       note: Max=up*mults, and enter odd numbers for type 1 filter
  wc : Cutoff frequency of the polyphase filter [0:pi]
Returns:
  Figure object
  Axes objects
###########################################################################
    """


###########################################################################
    # Class constructor
    def __init__(self,up,down,mults,filtTaps,wc):
        """
###########################################################################
                        PolyphaseResampler
Description: Polyphase resampler object for arbitrary resampling
             and interpolation using a polyphase filter
Arguments:
  up : Upsample amount
  down : Downsample amount
  mults : Number of multiplications allowed
  filtTaps : Number if filter taps to use in the polyphase filter
       note: Max=up*mults, and enter odd numbers for type 1 filter
  wc : Cutoff frequency of the polyphase filter [0:pi]
Returns:
  Figure object
  Axes objects
###########################################################################
        """
        
        #inital phase state
        self.phase=0
        
        #entered constants
        self.up=up
        self.down=down
        self.multipliers=mults
        
        #derived constants
        self.maxTaps=self.up*self.multipliers
        self.coeffs=self.__GenerateCoeffs(filtTaps,wc)
        self.delayLine=self.__InitDelay()
###########################################################################



###########################################################################
    # Initialize the delay line (Private Method)
    def __InitDelay(self):
        delayLine=[]
        for i in range(self.multipliers):
            delayLine.append(0)
        return delayLine
###########################################################################


###########################################################################
    # Generate filter coefficients (Private Method)
    def __GenerateCoeffs(self,filtTaps,wc):
        coeffs=sig.firwin(filtTaps,wc,fs=2*math.pi,window='blackmanharris')
        coeffList=[]
        for coeff in coeffs:
            coeffList.append(coeff)
        while(len(coeffList)<self.maxTaps):
            coeffList.append(0)
        return coeffList
###########################################################################


###########################################################################
    # Add new sample to the delay line (Private Method)
    def __InsertNewSample(self,sample):
        newLine=[sample]
        for i in range(len(self.delayLine)-1):
            newLine.append(self.delayLine[i])
        self.delayLine=newLine
###########################################################################


###########################################################################
    # Calculate the output of the filter (Private Method)
    def __CalculateOutput(self):
        sum=0
        i=0
        for val in self.delayLine:
            sum+=self.coeffs[self.phase+i*self.up]*float(val)
            i+=1
        return sum
###########################################################################


###########################################################################
    # Process a new input sample
    def ProcessNewSample(self,sample):
        """
###########################################################################
                        ProcessNewSample
Description: Input a new sample into the filter and calculate output
             sample(s)
Arguments:
  sample : Sample value to input
Returns:
  A list of output samples. This list can be empty if a sample is dropped
###########################################################################
        """
        outList=[]
        self.__InsertNewSample(sample)
        if(self.up<self.down):
            if(self.phase<self.up):
                outList.append(self.__CalculateOutput())
                self.phase+=self.down-self.up
            else:
                self.phase-=self.up
        elif(self.up>self.down):
            if(self.phase>=self.up):
                self.phase-=self.up
            outList.append(self.__CalculateOutput())
            self.phase+=self.down
            while(self.phase<self.up):
                outList.append(self.__CalculateOutput())
                self.phase+=self.down
        else:
            self.phase=0
            outList.append(self.__CalculateOutput())
        return outList
###########################################################################


###########################################################################
    # Return the filter coefficients
    def GetFilterCoeffs(self):
        """
###########################################################################
                        GetFilterCoeffs
Description: Return the list of filter coefficients
Arguments:
    None
Returns:
  A list of FIR filter coefficients
###########################################################################
        """
        return self.coeffs
###########################################################################


###########################################################################
    # Get new filter coefficients based on a new number of taps and wc
    def UpdateFilterCoeffs(self,filtTaps,wc):
        """
###########################################################################
                        UpdateFilterCoeffs
Description: Update filter coefficients based on a new number of taps and
             wc
Arguments:
  filtTaps : Number if filter taps to use in the polyphase filter
       note: Max=up*mults, and enter odd numbers for type 1 filter
  wc : Cutoff frequency of the polyphase filter [0:pi]
###########################################################################
        """
        self.coeffs=self.__GenerateCoeffs(filtTaps,wc)
        self.delayLine=self.__InitDelay()
        self.phase=0
###########################################################################


###########################################################################
    # Manualy entered filter coefficients
    def ManualFilterCoeffs(self,b):
        """
###########################################################################
                        ManualFilterCoeffs
Description: Update filter coefficients based on a manual coefficients
Arguments:
  b : a list of filter coefficients
###########################################################################
        """
        newCoeffs=[]
        for val in b:
            newCoeffs.append(val)
        while(len(newCoeffs)<self.maxTaps):
            newCoeffs.append(0)
        self.coeffs=newCoeffs
        self.delayLine=self.__InitDelay()
        self.phase=0
###########################################################################


###########################################################################
    # Update the down sample amount
    def UpdateDownSample(self,down):
        """
###########################################################################
                        UpdateDownSample
Description: Update downsample amount in filter
Arguments:
  down : New downsample amount
###########################################################################
        """
        self.down=down
        self.phase=0
###########################################################################