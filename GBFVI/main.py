from FVI import FVI
'''
   loss can be LS,LAD or Huber
   transfer can be 0 or 1
   number_of_iterations can be set (default=10)
'''
#FVI(simulator="logistics",number_of_iterations=100) #logistics default
#FVI(simulator="blocks",transfer=1,trees=10,number_of_iterations=100) #blocksworld
#FVI(simulator="pong",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #pong --> uncomment import statements from FVI.py
#FVI(simulator="tetris",trees=1,loss="LS",number_of_iterations=20) #tetris --> uncomment import stmts from FVI.py
#FVI(simulator="wumpus",transfer=1,trees=10,number_of_iterations=100) #wumpusworld
FVI(simulator="blackjack",transfer=1,number_of_iterations=100) #no facts in 1 trajectory => (batch_size=10)
#FVI(simulator="50chain",batch_size=2,trees=1,loss="LS",number_of_iterations=20) #for simple domains 10 trees not required
#FVI(simulator="net_admin") #network administrator domain
