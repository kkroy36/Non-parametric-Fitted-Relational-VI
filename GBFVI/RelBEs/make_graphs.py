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
'''
with open(domain+"_GBLSBEs.txt") as f:
    gbls = f.read().splitlines()
    gbls = [item.split(":")[2] for item in gbls]
with open(domain+"_GBLADBEs.txt") as f:
    gblad = f.read().splitlines()
    gblad = [item.split(":")[2] for item in gblad]
with open(domain+"_GBHuberBEs.txt") as f:
    gbhuber = f.read().splitlines()
    gbhuber = [item.split(":")[2] for item in gbhuber]
'''
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
    wotr = file[:20]
    wtr = file[20:]
    

plt.ylim(ymin=-0.02,ymax=0.2)
plt.plot(range(20),wotr,label="without transfer",color='red',linewidth=3)
plt.plot(range(20),wtr,label="with transfer",color='green',linewidth=3)
#plt.plot(range(20),difference(gbhuber,gbls),label="LAD",color='red',linewidth=3)
#plt.plot(range(20),difference(gbhuber,ls),label="LS",color='green',linewidth=3)

plt.xlabel("iterations")
plt.ylabel("average of the bellman error")
plt.title(domain)
plt.legend(prop={'size': 20})
plt.show()

