from __future__ import print_function

from Utils import Utils
from Tree import node
from Boosting import Boosting
from sys import argv
from os import system

class GradientBoosting(object):

    def __init__(self,regression=False,trees=10,treeDepth=2,loss="LS",sampling_rate=1.0):
        self.targets = None
        self.regression = regression
        self.sampling_rate = sampling_rate
        self.numberOfTrees = trees
        self.treeDepth = treeDepth
        self.trees = {}
        self.data = None
        self.loss = loss
        self.testPos,self.testNeg,self.testExamples = {},{},{}

    def setTargets(self,targets):
        self.targets = targets

    def learn(self,facts,examples,bk):
        for target in self.targets:
            data = Utils.setTrainingData(target=target,facts=facts,examples=examples,bk=bk,regression=self.regression,sampling_rate = self.sampling_rate)
            trees = []
            for i in range(self.numberOfTrees):
                print ('='*20,"learning tree",str(i),'='*20)
                node.setMaxDepth(self.treeDepth)
                node.learnTree(data)
                trees.append(node.learnedDecisionTree)
                Boosting.updateGradients(data,trees,loss=self.loss)
        self.trees[target] = trees
        for tree in trees:
            print ('='*30,"tree",str(trees.index(tree)),'='*30)
            for clause in tree:
                print (clause)

    def infer(self,facts,examples):
        self.testExamples = {}
        for target in self.targets:
            data = Utils.setTestData(target=target,facts=facts,examples=examples,regression=self.regression)
            Boosting.performInference(data,self.trees[target])
            self.testExamples[target] = data.examples
            print (data.examples)
