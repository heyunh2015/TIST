import support
import operator, copy

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

def meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict):
    meshTermsDictCopy = copy.deepcopy(meshTermsDict)
    for meshTerm in meshTermsDict:
        if meshTerm in meshTermSynonymDict:
            for meshTermSynonym in meshTermSynonymDict[meshTerm]:
                meshTermsDictCopy[meshTermSynonym] = 1
    #support.printDict(meshTermsDict, 2)
    return meshTermsDictCopy

def loadMeshTermsSynonym():
    meshTermSynonymDict = {}
    meshTermSynonymFile = 'I:\\bibm2016\\experiments\\mesh\\MeSHWords.txt'
    fp = open(meshTermSynonymFile)
    for line in fp.readlines():
        lineArr = line.strip().split(':')
        meshTerm = support.removePunctuation(lineArr[0])
        if meshTerm not in meshTermSynonymDict:
            meshTermSynonymDict[meshTerm] = {}
        meshTermSynonymList = lineArr[1].strip('|').split('|')
        meshTermSynonymNumber = len(meshTermSynonymList)-1
        if meshTermSynonymNumber>0:
            for meshTermSynonymIndex in range(1, meshTermSynonymNumber+1):
                meshTermSynonym = support.removePunctuation(meshTermSynonymList[meshTermSynonymIndex])
                meshTermSynonymDict[meshTerm][meshTermSynonym] = 1
                
    #support.printDict(meshTermSynonymDict, 1)
    return meshTermSynonymDict

def collectExpansionMeshTerms(titleFile, snipFile, hasSynonym):
    stopWordMeshTermDict = {'pain', 'disease'}
    meshTermsDict = support.loadMeshTerms('disease')
    if hasSynonym=='hasSynonym':
        meshTermSynonymDict = loadMeshTermsSynonym()
        meshTermsDict = meshTermDictAddSynonym(meshTermsDict, meshTermSynonymDict) 
    
    fpTitle = open(titleFile)
    fpSnip = open(snipFile)
    expansionMeshWordsCollect = {}
    for line in fpTitle.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit() and lineArr[0] not in expansionMeshWordsCollect:
                queryId = lineArr[0]
                expansionMeshWordsCollect[queryId] = {}
            else:
                titleSentence = support.removePunctuation(lineArr[1])
                titleSentenceLower = support.sentenceLower(titleSentence)
                for meshTerm in meshTermsDict:
                    #reMesh = re.compile(meshTerm)  
                    #numberMeshTerm = len(reMesh.findall(titleSentenceLower))        
                    #if numberMeshTerm!=0:
                     #   expansionWordsCollect[queryId][meshTerm] = numberMeshTerm
                    if meshTerm not in expansionMeshWordsCollect[queryId] and titleSentenceLower.find(meshTerm)!=-1 and meshTerm not in stopWordMeshTermDict:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
                        
    for line in fpSnip.readlines():
        if line.strip()!='':
            lineArr = line.strip().split('\t')
            if lineArr[0].isdigit():
                queryId = lineArr[0]
            else:
                snipSentence = support.removePunctuation(lineArr[1])
                snipSentenceLower = support.sentenceLower(snipSentence)
                for meshTerm in meshTermsDict:
                    if meshTerm not in expansionMeshWordsCollect[queryId] and snipSentenceLower.find(meshTerm)!=-1 and meshTerm not in stopWordMeshTermDict:
                        expansionMeshWordsCollect[queryId][meshTerm] = 0
    
    return expansionMeshWordsCollect

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

def expansionWordsAddTfIdfInformation(expansionWordsCollect):
    queryTermCount, queryTermInverseDoumentfreq = expansionWordsTfIdf(expansionWordsCollect)
    for queryId in expansionWordsCollect:
        for word in expansionWordsCollect[queryId]:
            idf = 0.0
            tf = 0.0
            idf = queryTermInverseDoumentfreq[word]
            tf = expansionWordsCollect[queryId][word]*1.0/queryTermCount[queryId]
            expansionWordsCollect[queryId][word] = tf*idf
    
    return expansionWordsCollect

def meshExpansionWordsAddstatisticInformation(expansionWordsCollect, expansionMeshWordsCollect):
    
    queryTermCount, queryTermInverseDoumentfreq = expansionWordsTfIdf(expansionWordsCollect)
                
    
    for queryId in range(1,len(expansionWordsCollect)+1):
        for word in expansionMeshWordsCollect[str(queryId)]:
            idf = 0.0
            tf = 0.0
            if word in expansionWordsCollect[str(queryId)]:
                idf = queryTermInverseDoumentfreq[word]
                tf = expansionWordsCollect[str(queryId)][word]*1.0/queryTermCount[str(queryId)]
                expansionMeshWordsCollect[str(queryId)][word] = tf*idf
            else:
                wordList = word.strip().split(' ')
                for wordSingle in wordList:
                    if wordSingle in expansionWordsCollect[str(queryId)]:
                        tf += expansionWordsCollect[str(queryId)][wordSingle]
                        idf += queryTermInverseDoumentfreq[wordSingle]
                    else:
                        tf = 1.0
                        idf = 0.1
                idf = idf/len(wordList)     
                tf = tf*1.0/len(wordList)/queryTermCount[str(queryId)]
                expansionMeshWordsCollect[str(queryId)][word] = tf*idf  
            
    return expansionMeshWordsCollect

def selectExpansionWordsByNormalTfIdf(expansionWordsCollect, termCountThreshold, termRankThreshold):
    expansionWordsCollectNormal = {}
    
    for queryId in expansionWordsCollect:
        ZNormal = 0.0
        expansionWordsCollectNormal[queryId] = {}
        for word in expansionWordsCollect[queryId]:
            ZNormal += expansionWordsCollect[queryId][word]
        for word in expansionWordsCollect[queryId]:
            expansionWordsCollectNormal[queryId][word] = expansionWordsCollect[queryId][word]*1.0/ZNormal
            
    expansionWordsSelect = {}
    for queryId in expansionWordsCollectNormal:
        NormalZ = 0.0
        if queryId not in expansionWordsSelect:
            expansionWordsSelect[queryId] = {}
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
                    print queryId, item[0], item[1]
        #for expansionTerm in expansionWordsSelect[queryId]:
            #expansionWordsSelect[queryId][expansionTerm] = expansionWordsSelect[queryId][expansionTerm]/NormalZ
    expansionWordsNumber = 0
    for queryId in expansionWordsSelect:
        print queryId, expansionWordsSelect[queryId]
        expansionWordsNumber += len(expansionWordsSelect[queryId])
    print termRankThreshold, expansionWordsNumber*1.0/30
    return expansionWordsSelect

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

def adjustWeight(lowIndex, highIndex, unit, originalWords, expansionWordsSelect):
    for expansionWordsWeight in range(lowIndex, highIndex+1, unit):
        combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                expansionWordsWeight*1.0/10, 
                                                'I:\\bibm2016\\experiments\\cds2014\\query\\differentWeightAmongExpansionWords\\2014HowToScenarioGoogleMeshNormal_01_3_0'+str(expansionWordsWeight)+'.query')
    return 0

def adjustExpansionWordsNumber(expansionMeshWordsCollect):
    for expansionWordsNumber in range(1,10):
        expansionWordsSelect = selectExpansionWordsByNormalTfIdf(expansionMeshWordsCollect, 
                                                0.1, 
                                                expansionWordsNumber)
        combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                0.5, 
                                                'I:\\bibm2016\\experiments\\cds2014\\query\\expansionWordsNumber\\2014HowToScenarioGoogleMeshNormal_01_'+str(expansionWordsNumber)+'_05.query')
    return 0

if __name__ == "__main__":  
    expansionWordsCollect = collectExpansionWords('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Original\\parse_title.txt',
                          'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Original\\parse_snip.txt')

    originalWords = support.extractOriginalWords('I:\\bibm2016\\experiments\\cds2015\\query\\2015OriginalQuery.txt')
    
    expansionMeshWordsCollect = collectExpansionMeshTerms('I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Original\\parse_title.txt',
                          'I:\\bibm2016\\experiments\\GoogleSearch\\result\\2015Original\\parse_snip.txt',
                          'hasSynonym')  

    expansionMeshWordsCollect = meshExpansionWordsAddstatisticInformation(expansionWordsCollect, expansionMeshWordsCollect)
    #expansionWordsCollect = expansionWordsAddTfIdfInformation(expansionWordsCollect)
    
    expansionWordsSelect = selectExpansionWordsByNormalTfIdf(expansionMeshWordsCollect, 
                                                0.07, 
                                                3)
    
    combineExpansionOriginalWordsWeightDifferent(originalWords, 
                                                expansionWordsSelect, 
                                                0.5, 
                                                'I:\\bibm2016\\experiments\\cds2015\\query\\final2\\2015GoogleOriginalMeshSynonymNormal_007_3_05.query')
    #adjustWeight(1,9,1, originalWords, expansionWordsSelect)
    #adjustExpansionWordsNumber(expansionMeshWordsCollect)
    