from FVI import FVI
import sys
'''
   loss can be LS,LAD or Huber
   transfer can be 0 or 1
   number_of_iterations can be set (default=10)
'''
#log_file = open("log.txt","w")
#sys.stdout = log_file
FVI(simulator="logistics",trees=1,batch_size=1,number_of_iterations=1) #logistics default
#FVI(simulator="blocks",trees=1,batch_size=3,number_of_iterations=2) #blocksworld
#FVI(simulator="pong",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #pong --> uncomment import statements from FVI.py
#FVI(simulator="tetris",trees=1,loss="LS",number_of_iterations=20) #tetris --> uncomment import stmts from FVI.py
#FVI(simulator="wumpus",trees=3,batch_size=3,number_of_iterations=5) #wumpusworld
#FVI(simulator="blackjack",transfer=1,number_of_iterations=100) #no facts in 1 trajectory => (batch_size=10)
#FVI(simulator="50chain",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #for simple domains 10 trees not required
#FVI(simulator="net_admin",trees=1,batch_size=6,number_of_iterations=1) #network administrator domain
#log_file.close()