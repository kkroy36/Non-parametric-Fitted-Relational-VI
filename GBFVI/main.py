from FVI import FVI
'''
   loss can be LS,LAD or Huber
   transfer can be 0 or 1
   number_of_iterations can be set (default=10)
'''
#FVI(simulator="logistics",trees=1,loss="Huber",number_of_iterations=20) #logistics default
#FVI(simulator="blocks",trees=1,loss="Huber",number_of_iterations=20) #blocksworld
#FVI(simulator="pong",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #pong --> uncomment import statements from FVI.py
FVI(simulator="tetris",loss="Huber",number_of_iterations=20) #tetris --> uncomment import stmts from FVI.py
#FVI(simulator="wumpus",trees=1,loss="Huber",number_of_iterations=20) #wumpusworld
#FVI(simulator="blackjack",trees=1,batch_size=10,loss="Huber",number_of_iterations=20) #no facts in 1 trajectory => (batch_size=10)
#FVI(simulator="50chain",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #for simple domains 10 trees not required
#FVI(simulator="net_admin") #network administrator domain
