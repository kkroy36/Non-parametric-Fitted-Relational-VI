from FVI import FVI
#FVI() #logistics default
#FVI(simulator="blocks",transfer=1,loss="Huber") #blocksworld
#FVI(simulator="pong") #pong --> uncomment import statements from FVI.py
#FVI(simulator="tetris") #tetris --> uncomment import stmts from FVI.py
#FVI(simulator="wumpus") #wumpusworld
#FVI(simulator="blackjack",transfer=1,batch_size=10,loss="LAD") #no facts in 1 trajectory => (batch_size=10)
FVI(simulator="50chain",batch_size=2,trees=2) #for simple domains 10 trees not required
