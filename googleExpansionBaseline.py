# -*- coding: utf-8 -*- 
import re,operator,os,copy
import support as support
import numpy as np
from support import sampleEvalOnFolder

def collectExpansionWords(titleFile, snipFile):
    stopWordsDic = support.loadStopWord()
    fpTitle = open(titleFile)
    fpSnip = open(snipFile)
    expansionWordsCollect = {}
    for line in fpTitle.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in expansionWordsCollect:
                queryId = lineArr[0]
                expansionWordsCollect[queryId] = {}
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleWordsList = titleSentence.strip().split(' ')
                for word in titleWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = 1
                        else:
                            expansionWordsCollect[queryId][wordLower] += 1
                
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipWordsList = snipSentence.strip().split(' ')
                for word in snipWordsList:
                    wordLower = word.lower()
                    if not word.isdigit() and word!='' and support.isNotStopWords(wordLower, stopWordsDic):
                        if wordLower not in expansionWordsCollect[queryId]:
                            expansionWordsCollect[queryId][wordLower] = 1
                        else:
                            expansionWordsCollect[queryId][wordLower] += 1
                                
    return expansionWordsCollect

def expansionWordsAddTfIdfInformation(expansionWordsCollect):
    queryTermCount, queryTermInverseDoumentfreq = expansionWordsTfIdf(expansionWordsCollect)
    for queryId in expansionWordsCollect:
        for word in expansionWordsCollect[queryId]:
            idf = 0.0
            tf = 0.0
            idf = queryTermInverseDoumentfreq[word]
            tf = expansionWordsCollect[queryId][word]*1.0/queryTermCount[queryId]
            expansionWordsCollect[queryId][word] = tf#*idf
    
    return expansionWordsCollect

def expansionWordsTfIdf(expansionWordsCollect):
    queryTermCount = {}
    queryTermDoumentfreq = {}
    for query in expansionWordsCollect:
        queryTermCount[query] = 0
        for term in expansionWordsCollect[query]:
            queryTermCount[query] += expansionWordsCollect[query][term]
            if term not in queryTermDoumentfreq:
                queryTermDoumentfreq[term] = {}
            if query not in queryTermDoumentfreq[term]:
                queryTermDoumentfreq[term][query] = 1
    
    #print  queryTermCount[query]
              
    queryTermInverseDoumentfreq = {}
    queryCount = len(queryTermCount)
    for term in queryTermDoumentfreq:
        queryTermDoumentfreq[term] = len(queryTermDoumentfreq[term])
        queryTermInverseDoumentfreq[term] = queryCount*1.0/queryTermDoumentfreq[term]
        #print term, queryTermDoumentfreq[term]
    return queryTermCount, queryTermInverseDoumentfreq

def selectExpansionWordsByNormalTfIdf(expansionMeshWordsTfIdf, termCountThreshold, termRankThreshold):
    #meshTreeCodeDict = loadMeshTreeCode(MeshTreeField)
    expansionWordsCollectNormal = {}
    #stopWordMeshTermDict = {'fever','emergency'}
    for queryId in expansionMeshWordsTfIdf:
        ZNormal = 0.0
        expansionWordsCollectNormal[queryId] = {}
        for word in expansionMeshWordsTfIdf[queryId]:
            #if word not in stopWordMeshTermDict:
                ZNormal += expansionMeshWordsTfIdf[queryId][word]
        for word in expansionMeshWordsTfIdf[queryId]:
            #if word not in stopWordMeshTermDict:
                expansionWordsCollectNormal[queryId][word] = expansionMeshWordsTfIdf[queryId][word]*1.0/ZNormal
            
    expansionWordsSelect = {}
    expansionWordsDashboard = {}
    for queryId in expansionWordsCollectNormal:
        res = ''
        if queryId not in expansionWordsSelect:
            expansionWordsSelect[queryId] = {}
            expansionWordsDashboard[queryId] = {}
        count = 0
        sortExpansionTermsList = sorted(expansionWordsCollectNormal[queryId].iteritems(), key=operator.itemgetter(1), reverse=True)
        maxProb = sortExpansionTermsList[0][1]
        for item in sortExpansionTermsList: 
            #print queryId, item[0], item[1]
            itemList = item[0].split(' ')
            for itemSingle in itemList:
                if item[1] > termCountThreshold and count < termRankThreshold:
                    expansionWordsSelect[queryId][itemSingle] = item[1]/maxProb
                    count += 1
                    #NormalZ += item[1]
                    res += itemSingle+ ' '
                    #print queryId, item[0], item[1], count#, meshTreeCodeDict[item[0]]
                    if item[0] not in expansionWordsDashboard[queryId]:
                        expansionWordsDashboard[queryId][item[0]] = [item[1], count]
        print queryId, res
        res = ''
        #for expansionTerm in expansionWordsSelect[queryId]:
            #expansionWordsSelect[queryId][expansionTerm] = expansionWordsSelect[queryId][expansionTerm]/NormalZ
    expansionWordsNumber = 0
    for queryId in expansionWordsSelect:
        #print queryId, expansionWordsSelect[queryId]
        expansionWordsNumber += len(expansionWordsSelect[queryId])
    print termRankThreshold, expansionWordsNumber*1.0/30
    
    #support.printDict(expansionWordsDashboard, 2)
    return expansionWordsSelect, expansionWordsDashboard

def combineExpansionOriginalWordsWeightDifferent(originalWords, expansionWordsSelect, weightExpansionWords, combineQueryFile):
    queryExpansionContent = ''
    for queryId in range(1,len(originalWords)+1):
        queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
        lengthOrigialWords = len(originalWords[str(queryId)])
        #lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
        for originalWordIndex in range(lengthOrigialWords):  
            queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+'^'+str(1-weightExpansionWords)+' '#+'\n\n'+r'</top>'+'\n\n'
        for expansionWord in expansionWordsSelect[str(queryId)]:
            queryExpansionContent += expansionWord+'^'+str(weightExpansionWords*expansionWordsSelect[str(queryId)][expansionWord])+' '
        queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
    support.saveFile(queryExpansionContent.replace('xray', 'x-ray'), combineQueryFile)
    return 0

if __name__ == "__main__":  
    expansionWordsCollect = collectExpansionWords('I:\\bibm2016\\experiments\\GoogleSearch\\result\\HowToScenario2016\\parse_title.txt',
                          'I:\\bibm2016\\experiments\\GoogleSearch\\result\\HowToScenario2016\\parse_snip.txt')

    originalWords = support.extractOriginalWords('I:\\bibm2016\\experiments\\cds2016\\query\\2016OriginalQuery.txt')
    
    expansionWordsCollect = expansionWordsAddTfIdfInformation(expansionWordsCollect)
    
    expansionWordsSelect, expansionWordsDashboardBe = selectExpansionWordsByNormalTfIdf(expansionWordsCollect, 
                                                                                    0.001, 
                                                                                      3)
    
    combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                0.5,    
                                                'I:\\bibm2016\\experiments\\cds2016\\query\\final3\\webAssistance\\2016WebAssistanceTF_0001_3_05.query')