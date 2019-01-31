# Non-parametric-Fitted-Relational-VI


**Parameters**

1. simulator (can be 50chain, blackjack, pong, tetris, wumpus, blocks or logistics)

2. transfer (can be 0 or 1)

3. number_of_iterations

4. batch_size

5. loss (can be LS, LAD or Huber)

6. trees (number of trees)

*Example run: FVI(simulator="blocks",loss="Huber",number_of_iterations=10)*

**Summary of changes**

1. Discretized features in propositional domains. (Before propositional baselines were using continuous features)

2. Plotted new graphs in graphs folder

**Notes**

1. Results may differ due to high variance.

2. For stable results and to perform as per theoretical expectation best to *increase initial model computation iterations in compute transfer model function* and/or *increase batch size* and *fix the policy during comparison in the execute random action function present in all simulators*

contact: kxr150330@utdallas.edu

**This is still in development. So, please wait for a while until it is pefected. Go ahead and test the version that is there, I'd love to learn about more issues that the code might have**
