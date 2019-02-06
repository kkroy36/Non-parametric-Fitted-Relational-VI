from FVI import FVI
import sys
import numpy as np
'''
   loss can be LS,LAD or Huber
   transfer can be 0 or 1
   number_of_iterations can be set (default=10)
'''
#log_file = open("log.txt","w")

#sys.stdout = log_file
"""These parameters have to be mentioned by the user"""

"""Settings for experiments batch_size=10, no_of_iterations=50, trees=1 (baseline), 3, 5, no_of_runs=5 & 10"""
"""Sample path: C:\Users\sxd170431\Desktop\Work\Projects\Relational_RL\Results\logistics\Runs_1\Policy_0.9\trees_3\LS"""

path="C://Users//sxd170431//Desktop//Work//Projects//Relational_RL//Results//"
no_of_runs=5
policy=0.9
no_of_state_actions_average=50
test_trajectory_length=50
#length_start_state=[]

"""Data structures for capturing values accross the runs"""
all_run_bellman_error=[]
all_run_test_error=[]
all_run_true_values=[]
all_run_infered_values=[]
all_run_test_error_start=[]
all_run_true_values_start=[]
all_run_infered_values_start=[]
np.set_printoptions(threshold=np.inf)

for run in range(0,no_of_runs):
  print "Beginning run no", run  
  model=FVI(simulator="logistics",trees=3,batch_size=5,number_of_iterations=50, path=path,runs=no_of_runs, policy=policy,run_latest=run,loss="LAD",test_trajectory_length=test_trajectory_length) #logistics default
  """Statistics for a single run"""
  all_run_bellman_error.append(model.bellman_error)
  
  """Averages over first 50 (s,a) pairs. This variable can be changes"""
  all_run_test_error.append(model.test_error_state_action[0:no_of_state_actions_average])
  all_run_true_values.append(model.true_state_action_val[0:no_of_state_actions_average])
  all_run_infered_values.append(model.inf_state_action_val[0:no_of_state_actions_average])
  """Statistics for keeping the Q(s,a) of the start state of every trajectory"""
  all_run_test_error_start.append(model.test_start_error_state_action[0:test_trajectory_length-5])
  all_run_true_values_start.append(model.true_start_state_action_val[0:test_trajectory_length-5])
  all_run_infered_values_start.append(model.inf_start_state_action_val[0:test_trajectory_length-5])
  #FVI(simulator="blocks",trees=1,batch_size=3,number_of_iterations=2) #blocksworld
  #FVI(simulator="pong",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #pong --> uncomment import statements from FVI.py
  #FVI(simulator="tetris",trees=1,loss="LS",number_of_iterations=20) #tetris --> uncomment import stmts from FVI.py
  #FVI(simulator="wumpus",trees=3,batch_size=3,number_of_iterations=5) #wumpusworld
  #FVI(simulator="blackjack",transfer=1,number_of_iterations=100) #no facts in 1 trajectory => (batch_size=10)
  #FVI(simulator="50chain",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #for simple domains 10 trees not required
  #FVI(simulator="net_admin",trees=1,batch_size=6,number_of_iterations=1) #network administrator domain
  
resultpath=path+model.simulator+"//Runs_"+str(no_of_runs)+"//Policy_"+str(policy)+"//trees_"+str(model.trees)+"//"+model.loss+"//"
print all_run_test_error
"""Average the results across each run"""
all_run_bellman_error_avg=np.mean(all_run_bellman_error,axis=0)
all_run_test_error_avg=np.mean(all_run_test_error,axis=0)
all_run_true_values_avg=np.mean(all_run_true_values,axis=0)
all_run_infered_values_avg=np.mean(all_run_infered_values,axis=0)
all_run_test_error_start_avg=np.mean(all_run_test_error_start,axis=0)
all_run_true_values_start_avg=np.mean(all_run_true_values_start,axis=0)
all_run_infered_values_start_avg=np.mean(all_run_infered_values_start,axis=0)

"""Write all the statistics to a text file"""
np.savetxt(resultpath+'avg_bellman_error.txt',all_run_bellman_error_avg)
np.savetxt(resultpath+'avg_test_error.txt',all_run_test_error_avg)
np.savetxt(resultpath+'avg_true_val.txt',all_run_true_values_avg)
np.savetxt(resultpath+'avg_inf_val.txt',all_run_infered_values_avg)
np.savetxt(resultpath+'avg_test_error_start.txt',all_run_test_error_start_avg)
np.savetxt(resultpath+'avg_true_val_start.txt',all_run_true_values_start_avg)
np.savetxt(resultpath+'avg_inf_val_start.txt',all_run_infered_values_start_avg)






