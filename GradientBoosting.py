from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
from sys import argv

class GradientBoosting(object):
    '''class for performing gradient boosting'''

    def __init__(self,regression=False,trees=10,treeDepth=2):
        '''class constructor'''
        self.targets = None
        self.regression = regression
        self.numberOfTrees = trees
        self.treeDepth = treeDepth
        self.trees =  {}
        self.data = None
        self.testPos = {}
        self.testNeg = {}
        self.testExamples = {}

    def setTargets(self,targets):
        '''sets targets for classfication/regression'''
        self.targets = targets

    def learn(self,loss = "LS"):
        '''learns the model based on training data'''
        for target in self.targets:
            data = Utils.readTrainingData(target,self.regression)
            trees = []
            for i in range(self.numberOfTrees):
                print ('='*20,"learning tree",str(i),'='*20)
                node.setMaxDepth(self.treeDepth)
                node.learnTree(data)
                trees.append(node.learnedDecisionTree)
                Boosting.updateGradients(data,trees,loss=loss)
            self.trees[target] = trees
            for tree in trees:
                print ('='*30,"tree",str(trees.index(tree)),'='*30)
                for clause in tree:
                    print (clause)

    def infer(self):
        '''infers probability or regression value'''
        for target in self.targets:
            testData = Utils.readTestData(target,self.regression)
            Boosting.performInference(testData,self.trees[target])
            self.testPos[target] = testData.pos
            self.testNeg[target] = testData.neg
            self.testExamples[target] = testData.examples
            print (testData.pos)
            print (testData.neg)
            print (testData.examples)
