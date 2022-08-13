##f=open("C:\Users\Justin Killam\Documents\Git_Local\Python\Const.txt",'w')
depth=range(64)
val="("
fmt="x\"{0:08X}\""
for i in depth:
    val+=fmt.format(i*i*i*i)
    if i!=depth[-1]:
        val+=","
val+=");"
print(val)