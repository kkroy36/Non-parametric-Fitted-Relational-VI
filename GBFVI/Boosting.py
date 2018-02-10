from Utils import Utils
from math import log,exp
from Logic import Prover
from copy import deepcopy
import sklearn.metrics as sk
class Boosting(object):
    '''boosting class'''
    
    logPrior = log(0.1192/float(1-0.1192))

    @staticmethod
    def computeAdviceGradient(example):
        '''computes the advice gradients as nt-nf'''
        nt,nf = 0,0
        target = Utils.data.target.split('(')[0]
        for clause in Utils.data.adviceClauses:
            if Prover.prove(Utils.data,example,clause):
                if target in Utils.data.adviceClauses[clause]['preferred']:
                    nt += 1
                if target in Utils.data.adviceClauses[clause]['nonPreferred']:
                    nf += 1
        return (nt-nf)

    @staticmethod
    def inferTreeValue(clauses,query,data):
        '''returns probability of query
           given data and clauses learned
        '''
        for clause in clauses: #for every clause in the tree
            clauseCopy = deepcopy(clause)
            clauseValue = float(clauseCopy.split(" ")[1])
            clauseRule = clauseCopy.split(" ")[0].replace(";",",")
            if not clauseRule.split(":-")[1]:
                return clauseValue
            if Prover.prove(data,query,clauseRule): #check if query satisfies clause
                return clauseValue
    
    @staticmethod
    def computeSumOfGradients(example,trees,data):
        '''computes new gradient for example'''
        sumOfGradients = 0
        for tree in trees: #add leaf values satisfied by example in each tree
            gradient = Boosting.inferTreeValue(tree,example,data)
            print ("value of example: ",gradient)
            if gradient != None:
                sumOfGradients += gradient
        return sumOfGradients #return the sum

    @staticmethod
    def updateGradients(data,trees,loss="LS",delta=10):
        '''updates the gradients of the data'''
        if not data.regression:
            logPrior = Boosting.logPrior
            #P = sigmoid of sum of gradients given by each tree learned so far
            for example in data.pos: #for each positive example compute 1 - P
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
                updatedGradient = 1 - probabilityOfExample
                if data.advice:
                    adviceGradient = Boosting.computeAdviceGradient(example)
                    updatedGradient += adviceGradient
                data.pos[example] = updatedGradient
            for example in data.neg: #for each negative example compute 0 - P
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                probabilityOfExample = Utils.sigmoid(logPrior+sumOfGradients)
                updatedGradient = 0 - probabilityOfExample
                if data.advice:
                    adviceGradient = Boosting.computeAdviceGradient(example)
                    updatedGradient += adviceGradient
                data.neg[example] = updatedGradient
        if data.regression:
            for example in data.examples: #compute gradient as y-y_hat
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,data)
                trueValue = data.getExampleTrueValue(example)
                exampleValue = sumOfGradients
                if loss == "LS":
                    updatedGradient = trueValue - exampleValue
                    data.examples[example] = updatedGradient
                elif loss == "LAD":
                    updatedGradient = 0
                    gradient = trueValue - exampleValue
                    if gradient:
                        updatedGradient = gradient/float(abs(gradient))
                    data.examples[example] = updatedGradient
                elif loss == "Huber":
                    gradient = trueValue - exampleValue
                    updatedGradient = 0
                    if gradient:
                        if gradient > float(delta):
                            updatedGradient = gradient/float(abs(gradient))
                        elif gradient <= float(delta):
                            updatedGradient = gradient
                    data.examples[example] = updatedGradient

    @staticmethod
    def computeResults(testData):
        '''computes accuracy,AUC-ROC and AUC-PR'''
        yactual = [1 for i in range(len(list(testData.pos.values())))] + [0 for i in range(len(list(testData.neg.values())))]
        ypred = [int(x >= 0.5) for x in list(testData.pos.values())+list(testData.neg.values())]
        print ("accuracy: ",sk.accuracy_score(yactual,ypred))
        print ("AUC-ROC: ",sk.roc_auc_score(yactual,ypred))
        print ("AUC-PR: ",sk.average_precision_score(yactual,ypred))
        print ("Precision: ",sk.precision_score(yactual,ypred))
        print ("Recall: ",sk.recall_score(yactual,ypred))
        print ("F1: ",sk.f1_score(yactual,ypred))
               
    @staticmethod
    def performInference(testData,trees):
        '''computes probability for test examples'''
        logPrior = Boosting.logPrior
        if not testData.regression:
            logPrior = Boosting.logPrior #initialize log odds of assumed prior probability for example
            for example in testData.pos:
                print ("testing example: ",example)
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
                testData.pos[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
            for example in testData.neg:
                print ("testing example: ",example)
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData) #compute sum of gradients
                testData.neg[example] = Utils.sigmoid(logPrior+sumOfGradients) #calculate probability as sigmoid(log odds)
        elif testData.regression:
            for example in testData.examples:
                sumOfGradients = Boosting.computeSumOfGradients(example,trees,testData)
                testData.examples[example] = sumOfGradients
        #Boosting.computeResults(testData)
