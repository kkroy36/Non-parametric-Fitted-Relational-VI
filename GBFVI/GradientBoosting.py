from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
from sys import argv
from os import system

class GradientBoosting(object):

    def __init__(self,regression=False,trees=10,treeDepth=2):
        self.targets = None
        self.regression = regression
        self.numberOfTrees = trees
        self.treeDepth = treeDepth
        self.trees = {}
        self.data = None
        self.testPos,testNeg,testExamples = {},{},{}

    def setTargets(self,targets):
        self.targets = targets

    def learn(self,facts,examples,bk):
        for target in self.targets:
            data = Utils.setTrainingData(target=target,facts=facts,examples=examples,bk=bk,regression=True)
            trees = []
            for i in range(self.numberOfTrees):
                print ('='*20,"learning tree",str(i),'='*20)
                node.setMaxDepth(self.treeDepth)
                node.learnTree(data)
                trees.append(node.learnedDecisionTree)
                Boosting.updateGradients(data,trees)
        self.trees[target] = trees
        for tree in trees:
            print ('='*30,"tree",str(trees.index(tree)),'='*30)
            for clause in tree:
                print (clause)
'''
def main():
    #main method
    targets = argv[argv.index("-target")+1][1:-1].split(',') #read targets from input
    sampling_rate_train = 100
    sampling_rate_test = 100
    regression,advice = False,False
    if "-reg" in argv:
        regression = True
    if "-expAdvice" in argv:
        advice = True
    if "-samplingratetrain" in argv:
        sampling_rate_train = int(argv[argv.index("-samplingratetrain")+1][1:-1])
    if "-samplingratetest" in argv:
        sampling_rate_test = int(argv[argv.index("-samplingratetest")+1][1:-1])
    for target in targets:
        data = Utils.readTrainingData(target,sampling_rate_train,regression,advice) #read training data
        numberOfTrees = 10 #number of trees for boosting
        trees = [] #initialize place holder for trees
        for i in range(numberOfTrees): #learn each tree and update gradient
            print('='*20,"learning tree",str(i),'='*20)
            node.setMaxDepth(6)
            node.learnTree(data) #learn RRT
            #print ("dot file: ",node.learnedDotFile)
            #exit()
            trees.append(node.learnedDecisionTree)
            Boosting.updateGradients(data,trees)
        for tree in trees:
            print('='*30,"tree",str(trees.index(tree)),'='*30)
            for clause in tree:
                print(clause)
        testData = Utils.readTestData(target,sampling_rate_test,regression) #read testing data
        Boosting.performInference(testData,trees) #get probability of test examples
        system("rm *.pyc")
        #print (testData.pos) #--> uncomment to see test query probabilities (for classification)
        #print (testData.neg)

        #print testData.examples #--> uncomment to see test example values (for regression)
'''

#main()
