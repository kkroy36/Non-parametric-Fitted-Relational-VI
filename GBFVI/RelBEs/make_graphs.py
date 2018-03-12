import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from math import log
from sys import argv

matplotlib.rcParams.update({'font.size':26})

def difference(l1,l2):
    '''returns difference between the lists'''
    N = len(l1)
    return [(float(l1[i])-float(l2[i])) for i in range(N)]

domain = argv[argv.index("-domain")+1]

gbls,gbhuber,gblad,nn,ls,rrt,wtr,wotr = [],[],[],[],[],[],[],[]

with open(domain+"_GBLSBEs.txt") as f:
    gbls = f.read().splitlines()
    gbls = [item.split(":")[2] for item in gbls]

with open(domain+"_GBLADBEs.txt") as f:
    gblad = f.read().splitlines()
    gblad = [item.split(":")[2] for item in gblad]
    
with open(domain+"_GBHuberBEs.txt") as f:
    gbhuber = f.read().splitlines()
    gbhuber = [item.split(":")[2] for item in gbhuber]

with open(domain+"_RRTBEs.txt") as f:
    rrt = f.read().splitlines()
    rrt = [item.split(":")[2] for item in rrt]

'''
with open(domain+"_NNBEs.txt") as f:
    nn = f.read().splitlines()
    nn = [item.split("[")[1][:-1] for item in nn]
with open(domain+"_LSBEs.txt") as f:
    ls = f.read().splitlines()
    ls = [item.split("[")[1][:-1] for item in ls]
'''
with open(domain+"_transferBEs.txt") as f:
    file = f.read().splitlines()
    file = [float(item.split(":")[2]) for item in file]
    wotr = file[:100]
    wtr = file[100:]
    
'''
print (sum([int(float(x)>3) for x in gbhuber]))
print (sum([int(float(x)>3) for x in gbls]))
print (sum([int(float(x)>3) for x in gblad]))
'''
#print (sum([int(float(x)>5) for x in wotr]))
#print (sum([int(float(x)>5) for x in wtr]))
plt.ylim(ymin=0,ymax=8)
#plt.plot(range(100),difference(rrt,gbhuber),label="RRT",color='blue',linewidth=3)
#plt.plot(range(100),difference(gbls,gbhuber),label="LS",color='green',linewidth=3)
#plt.plot(range(100),difference(gblad,gbhuber),label="LAD",color='red',linewidth=3)
plt.plot(range(100),wtr,label="with transfer",color='green',linewidth=3)
plt.plot(range(100),wotr,label="without transfer",color='red',linewidth=3)
plt.xlabel("iterations")
plt.ylabel("average of the bellman error")
plt.title(domain)
plt.legend(prop={'size': 20})
plt.show()

