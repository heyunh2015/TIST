#! /usr/bin/python
# -*- coding: utf-8 -*- 
import os

def submitQueryWeight(lowIndex, highIndex, unit):
    for weightOriginal in range(lowIndex, highIndex+1, unit):
        cmdStr = 'trec_terrier.sh -r -Dtrec.model=BM25 -c 0.75 -Dtrec.topics=/home/lmy/bibm2016/2014cds/query/differentWeightAmongExpansionWords/2014HowToScenarioGoogleMeshNormal_01_3_0'+str(weightOriginal)+'.query' 
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0

def submitQueryExpansionNumber(lowIndex, highIndex, unit):
    for expansionNumber in range(lowIndex, highIndex+1, unit):
        cmdStr = 'trec_terrier.sh -r -Dtrec.model=BM25 -c 0.75 -Dtrec.topics=/home/lmy/bibm2016/2014cds/query/expansionWordsNumber/2014HowToScenarioGoogleMeshNormal_01_'+str(expansionNumber)+'_05.query' 
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0

def submitQueryProgressControl(lowIndex, highIndex, unit):
    for progressControl in range(lowIndex, highIndex+1, unit):
        cmdStr = 'trec_terrier.sh -r -Dtrec.model=BM25 -c 0.75 -Dtrec.topics=/home/lmy/bibm2016/2015cds/query/final3/progressControlTfIdf/2015HowToScenarioGoogleTfIdfMeshSynonymNormal_001_3_05_'+str(progressControl)+'.query' 
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    
    return 0
if __name__ == "__main__":
    #submitQueryWeight(1,9,1)
    #submitQueryExpansionNumber(1,9,1)
    submitQueryProgressControl(1,20,1)