# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:13:13 2019

@author: sxd170431
"""
import numpy as np
import matplotlib.pyplot as plt

path="C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//logistics//Runs_30//Policy_0//trees_3//LS//"
all_run_bellman_error_max = []
all_run_bellman_error_mean=[]
all_run_rmse_train = []
all_run_test_error=[]
all_run_true_values=[]
all_run_infered_values=[]
all_run_rmse_train = []
all_run_rmse_test = []

#for run in range(0,30):
    #path="C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//logistics//Runs_30//Policy_0//trees_5//LS//Run"+str(run)+"//"
#    with open(path+"logistics_BEs.txt") as fp:
#      BE_max = fp.read().splitlines()
#      BE_max = [float(item.split(':')[2]) for item in BE_max]
#    BE_max = np.array(BE_max)
#    all_run_bellman_error_max.append(BE_max)
    
    #rmse_train=np.genfromtxt(path+"rmse_train_error.txt")
    #all_run_rmse_train.append(rmse_train)
    #all_run_rmse_test.append(np.genfromtxt(path+"rmse_test_error.txt"))
    #all_run_bellman_error_max.append(np.genfromtxt(path+"bellman_error_avg.txt"))
    #all_run_bellman_error_mean.append(np.genfromtxt(path+"bellman_error_max.txt"))
    #all_run_test_error.append(np.genfromtxt(path+"testing_error.txt"))
    #all_run_true_values.append(np.genfromtxt(path+"true_values.txt"))
    #all_run_infered_values(np.genfromtxt(path+"inferred values.txt"))
resultpath="C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//blocks//Runs_1//Policy_0//trees_1//LS//"
all_run_bellman_error_mean_avg= np.genfromtxt(resultpath+"avg_bellman_error_mean.txt") 
all_run_bellman_error_max_avg=  np.genfromtxt(resultpath+"avg_bellman_error_max.txt")
all_run_rmse_train_avg=np.genfromtxt(resultpath+"avg_rmse_train.txt")
#all_run_bellman_error_mean_avg=np.mean(all_run_bellman_error_mean,axis=0)
#all_run_bellman_error_max_avg = np.mean(all_run_bellman_error_max,axis=0)
#all_run_test_error_avg=np.mean(all_run_test_error,axis=0)
#all_run_true_values_avg=np.mean(all_run_true_values,axis=0)
#all_run_infered_values_avg=np.mean(all_run_infered_values,axis=0)
#all_run_rmse_test_avg = np.mean(all_run_rmse_test,axis=0)
#all_run_rmse_train_avg = np.mean(all_run_rmse_train,axis=0)

resultpath="C:/Users/sxd170431/Desktop/Work//Projects//Relational_RL//Results//blocks//Runs_1//Policy_0//trees_1//LS//"

#np.savetxt(resultpath+'avg_bellman_error_mean.txt',all_run_bellman_error_mean_avg)
#np.savetxt(resultpath+'avg_bellman_error_max.txt',all_run_bellman_error_max_avg)
#np.savetxt(resultpath+'avg_test_error.txt',all_run_test_error_avg)
#np.savetxt(resultpath+'avg_true_val.txt',all_run_true_values_avg)
#np.savetxt(resultpath+'avg_inf_val.txt',all_run_infered_values_avg)
#np.savetxt(resultpath+'avg_rmse_test.txt',all_run_rmse_test_avg)
#np.savetxt(resultpath+'avg_rmse_train.txt',all_run_rmse_train_avg)
#print "The test rmse across all runs", all_run_rmse_test_avg

#BE_max = []
#with open(path+"avg_bellman_error_mean.txt") as fp:
#    BE_max = fp.read().splitlines()
#    BE_max = [float(item.split(':')[2]) for item in BE_max]
#BE_max = np.array(BE_max)
#BE_max=np.genfromtxt(path+"avg_bellman_error_mean.txt")

#all_run_bellman_error_max_avg=np.genfromtxt(resultpath+"avg_bellman_error_max.txt")
#all_run_bellman_error_mean_avg=np.genfromtxt(resultpath+"avg_bellman_error_mean.txt")
#all_run_rmse_train_avg=np.genfromtxt(resultpath+"avg_rmse_train.txt")

"""Blue color is for suggested algorithm accuracy"""
itertn=range(0,all_run_bellman_error_max_avg.shape[0])
plt.plot(itertn,all_run_bellman_error_max_avg,color='b',label='Max_Bellman_error')
plt.xlabel('No of value iteration')
plt.ylabel('Max Bellman error')
plt.legend()
plt.savefig(resultpath+'Avg_bellman_error_max.png', bbox_inches='tight')
plt.clf()

"""Blue color is for suggested algorithm accuracy"""
itertn=range(0,all_run_bellman_error_mean_avg.shape[0])
plt.plot(itertn,all_run_bellman_error_mean_avg,color='b',label='Avg_Bellman_error')
plt.xlabel('No of value iteration')
plt.ylabel('Mean Bellman error')
plt.legend()
plt.savefig(resultpath+'Avg_bellman_error_mean.png', bbox_inches='tight')
plt.clf()

"""Blue color is for suggested algorithm accuracy"""
itertn=range(0,all_run_rmse_train_avg.shape[0])
plt.plot(itertn,all_run_rmse_train_avg,color='b',label='RMSE_train_error')
plt.xlabel('No of value iteration')
plt.ylabel('RMSE_train')
plt.legend()
plt.savefig(resultpath+'rmse_train_error.png', bbox_inches='tight')
plt.clf()


