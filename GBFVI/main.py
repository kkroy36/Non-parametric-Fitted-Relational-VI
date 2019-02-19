from FVI import FVI
import sys
import os
import numpy as np
from shutil import rmtree
'''
   loss can be LS,LAD or Huber
   transfer can be 0 or 1
   number_of_iterations can be set (default=10)
'''
#log_file = open("log.txt","w")

#sys.stdout = log_file

"""Sample path: C:\Users\sxd170431\Desktop\Work\Projects\Relational_RL\Results\logistics\Runs_1\Policy_0.9\trees_3\LS"""

path="C://Users//sxd170431//Desktop//Work//Projects//Relational_RL//Results//"
#path="D://Grad Studies//Research//Relational RL//Results//"
#path="/home/kauroy/Desktop/Non-parametric-Fitted-Relational-VI-master/GBFVI/Results/"

"""*******************************************************************************************************"""
"""Parameters provided by user for running the Fitted Value Iteration Code"""
"""*******************************************************************************************************"""

simulator="logistics"
trees=5
batch_size=10
iters=50
loss="LS"
no_of_runs=30
policy=0
no_of_state_actions_average=30
test_trajectory_length=5
burn_in_no_of_traj=10
test_explore=0.1
treeDepth=1
"""*******************************************************************************************************"""

"""Data structures for collecting statistics accross the runs"""
all_run_bellman_error_mean=[]
all_run_bellman_error_max = []
all_run_test_error=[]
all_run_true_values=[]
all_run_infered_values=[]
all_run_test_error_start=[]
all_run_true_values_start=[]
all_run_infered_values_start=[]
#all_run_total_rewards = []
all_run_rmse_train = []
all_run_rmse_test = []
np.set_printoptions(threshold=np.inf)

"""Main Program begins here"""
for run in range(0,no_of_runs):
  #try:
      print "Beginning run no", run  
      resultpath=path+simulator+"//Runs_"+str(no_of_runs)+"//Policy_"+str(policy)+"//trees_"+str(trees)+"//"+loss+"//"
      ind_runpath=path+simulator+"//Runs_"+str(no_of_runs)+"//Policy_"+str(policy)+"//trees_"+str(trees)+"//"+loss+"//"+"Run"+str(run)+"//"
      """Deletes the previous run informations"""
      if (os.path.isdir(ind_runpath)):
          rmtree(ind_runpath)
      model=FVI(simulator=simulator,trees=trees,batch_size=batch_size,number_of_iterations=iters, path=path,runs=no_of_runs, policy=policy,run_latest=run,loss=loss,test_trajectory_length=test_trajectory_length,burn_in_no_of_traj=burn_in_no_of_traj,test_explore=0.1,treeDepth=treeDepth) #logistics default
      """Path where the results will be saved"""
      #resultpath=path+model.simulator+"/Runs_"+str(no_of_runs)+"/Policy_"+str(policy)+"/trees_"+str(model.trees)+"/"+model.loss+"/"
      """Statistics for a single run"""
      all_run_bellman_error_mean.append(model.bellman_error_avg)
      all_run_bellman_error_max.append(model.bellman_error_max)
      all_run_rmse_train.append(model.training_rmse)
      all_run_rmse_test.append(model.testing_rmse)
      """Averages over first 50 (s,a) pairs. This variable can be changes"""
      all_run_test_error.append(model.test_error_state_action[0:no_of_state_actions_average])
      all_run_true_values.append(model.true_state_action_val[0:no_of_state_actions_average])
      all_run_infered_values.append(model.inf_state_action_val[0:no_of_state_actions_average])
      """Statistics for keeping the Q(s,a) of the start state of every trajectory"""
      #all_run_test_error_start.append(model.test_start_error_state_action[0:test_trajectory_length-5])
      #all_run_true_values_start.append(model.true_start_state_action_val[0:test_trajectory_length-5])
      #all_run_infered_values_start.append(model.inf_start_state_action_val[0:test_trajectory_length-5])
      #FVI(simulator="blocks",trees=1,batch_size=3,number_of_iterations=2) #blocksworld
      #FVI(simulator="pong",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #pong --> uncomment import statements from FVI.py
      #FVI(simulator="tetris",trees=1,loss="LS",number_of_iterations=20) #tetris --> uncomment import stmts from FVI.py
      #FVI(simulator="wumpus",trees=3,batch_size=3,number_of_iterations=5) #wumpusworld
      #FVI(simulator="blackjack",transfer=1,number_of_iterations=100) #no facts in 1 trajectory => (batch_size=10)
      #FVI(simulator="50chain",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #for simple domains 10 trees not required
      #FVI(simulator="net_admin",trees=1,batch_size=6,number_of_iterations=1) #network administrator domain
      np.savetxt(ind_runpath+'rmse_train_error.txt',model.training_rmse)
      np.savetxt(ind_runpath+'rmse_test_error.txt',model.testing_rmse)
      np.savetxt(ind_runpath+'bellman_error_avg.txt',model.bellman_error_avg)
      np.savetxt(ind_runpath+'bellman_error_max.txt',model.bellman_error_max)
      with open(ind_runpath+'trajectory_and_mismatch_outputs.txt','a') as fp:
          for item in model.test_trajectories_output:
              fp.write(str(item)+"\n")
              fp.write('*'*80+"\n")
  #except:
      #print 'Run'+str(run)+'aborted'
      #continue
print "ALL THE RUN HAS FINISHED, NOW AVERAGING"  
"""Average the results across each run"""

all_run_bellman_error_mean_avg=np.mean(all_run_bellman_error_mean,axis=0)
all_run_bellman_error_max_avg = np.mean(all_run_bellman_error_max,axis=0)
all_run_test_error_avg=np.mean(all_run_test_error,axis=0)
all_run_true_values_avg=np.mean(all_run_true_values,axis=0)
all_run_infered_values_avg=np.mean(all_run_infered_values,axis=0)
#all_run_test_error_start_avg=np.mean(all_run_test_error_start,axis=0)
#all_run_true_values_start_avg=np.mean(all_run_true_values_start,axis=0)
#all_run_infered_values_start_avg=np.mean(all_run_infered_values_start,axis=0)
all_run_rmse_test_avg = np.mean(all_run_rmse_test,axis=0)
all_run_rmse_train_avg = np.mean(all_run_rmse_train,axis=0)

"""Write all the statistics to a text file"""
#np.savetxt(resultpath+'avg_total_rewards.txt',all_run_total_rewards_avg)
np.savetxt(resultpath+'avg_bellman_error_mean.txt',all_run_bellman_error_mean_avg)
np.savetxt(resultpath+'avg_bellman_error_max.txt',all_run_bellman_error_max_avg)
np.savetxt(resultpath+'avg_test_error.txt',all_run_test_error_avg)
np.savetxt(resultpath+'avg_true_val.txt',all_run_true_values_avg)
np.savetxt(resultpath+'avg_inf_val.txt',all_run_infered_values_avg)
#np.savetxt(resultpath+'avg_test_error_start.txt',all_run_test_error_start_avg)
#np.savetxt(resultpath+'avg_true_val_start.txt',all_run_true_values_start_avg)
#np.savetxt(resultpath+'avg_inf_val_start.txt',all_run_infered_values_start_avg)
np.savetxt(resultpath+'avg_rmse_test.txt',all_run_rmse_test_avg)
np.savetxt(resultpath+'avg_rmse_train.txt',all_run_rmse_train_avg)
print "The test rmse across all runs", all_run_rmse_test_avg






