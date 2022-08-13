outfile=open("DataDump.csv","w")
header="Index,AIN0,AIN1,AIN2\n"
rowfmt="%d,%d,%d,%d\n"

for i in range(5):
    outfile.write(rowfmt % (i*i,(i+1)*i,(i+2)*i,(i+3)*i))
outfile.close()