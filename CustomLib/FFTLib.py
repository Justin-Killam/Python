import numpy as np
import numpy.fft as fft

def FormattedFFT(vals,fs):
    ComplexRes=np.divide(fft.fftshift(fft.fft(vals)),len(vals))
    FreqVec=np.multiply(fft.fftshift(fft.fftfreq(len(vals))),fs)
    MagRes=np.absolute(ComplexRes)
    PhaseRes=np.angle(ComplexRes)
    return [ComplexRes,MagRes,PhaseRes,FreqVec]