# -*- coding: utf-8 -*-
"""
Created on Tue Mar 05 10:28:49 2019

@author: sxd170431
"""
import matplotlib.pyplot as plt
import numpy as np
trees=[5,7,10]
domain="logistics"
loss="Huber"
path="C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//"+domain+"//Runs_30//"
#C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//logistics//Runs_30//Policy_0//trees_10//Huber//Run"+str(run)+"//"
bellman_error_max=[]
bellman_error_mean=[]
for tree in trees:
    filepath=path+"Policy_0//trees_"+str(tree)+"//"+loss+"//"
    bellman_error_mean.append(np.genfromtxt(filepath+"avg_bellman_error_mean.txt"))
    bellman_error_max.append(np.genfromtxt(filepath+"avg_bellman_error_max.txt"))
onetreepath=path+"Policy_0//trees_1//LS//"
bellman_error_mean.append(np.genfromtxt(onetreepath+"avg_bellman_error_mean.txt")) 
bellman_error_max.append(np.genfromtxt(onetreepath+"avg_bellman_error_max.txt"))
   
"""Blue color is for suggested algorithm accuracy"""
itertn=range(0,bellman_error_max[0].shape[0])
plt.plot(itertn,bellman_error_max[0],color='b',label='tree5_'+loss)
plt.plot(itertn,bellman_error_max[1],color='g',label='tree7_'+loss)
plt.plot(itertn,bellman_error_max[2],color='r',label='tree10_'+loss)
plt.plot(itertn,bellman_error_max[3],color='c',label='tree1_LS')
plt.xlabel('No of value iteration')
plt.ylabel('Avg Bellman error max')
plt.legend()
plt.savefig(path+loss+'_avg_bellman_error_max.png', bbox_inches='tight')
plt.clf()

"""Blue color is for suggested algorithm accuracy"""
itertn=range(0,bellman_error_mean[0].shape[0])
plt.plot(itertn,bellman_error_mean[0],color='b',label='tree5_'+loss)
plt.plot(itertn,bellman_error_mean[1],color='g',label='tree7_'+loss)
plt.plot(itertn,bellman_error_mean[2],color='r',label='tree10_'+loss)
plt.plot(itertn,bellman_error_mean[3],color='c',label='tree1_LS')
plt.xlabel('No of value iteration')
plt.ylabel('Avg Bellman error mean')
plt.legend()
plt.savefig(path+loss+'_avg_bellman_error_mean.png', bbox_inches='tight')
plt.clf()
    