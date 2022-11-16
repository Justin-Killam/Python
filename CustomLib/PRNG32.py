def PRNG32(CurVal,Seed=0x2451AE31,Poly=0x80000062):
    feedback=0
    if(CurVal==0):
        CurVal=Seed
    else:
        for i in range(32):
            if(((Poly>>i)&1)==1):
                feedback=feedback^((CurVal>>i)&1)
        CurVal=(CurVal<<1)|feedback
    return CurVal