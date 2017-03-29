import support

def meshExpansion(originalWords, meshFile):
    meshExpansionWordsDict = {}
    meshTermSynonymDict = support.loadMeshTermsSynonym(meshFile)
    for queryId in originalWords:
        meshExpansionWordsDict[queryId] = []
        querySecntence = ' '
        for word in originalWords[queryId]:
            querySecntence += word + ' '
        for meshTerm in meshTermSynonymDict:
            for meshTermSynonymWord in meshTermSynonymDict[meshTerm]:
                if querySecntence.find(' ' + meshTermSynonymWord + ' ')!=-1:
                    meshExpansionWordsDict[queryId].append(meshTermSynonymDict[meshTerm])
                    break
    support.printDict(meshExpansionWordsDict, 1)
    return meshExpansionWordsDict

def combineExpansionOriginalWordsWeightSame(originalWords, expansionWordsSelect, hasWeight, weightExpansionWords, combineQueryFile):
    queryExpansionContent = ''
    if hasWeight=='no':
        for queryId in range(1,len(originalWords)+1):
            queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
            lengthOrigialWords = len(originalWords[str(queryId)])
            lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
            for originalWordIndex in range(lengthOrigialWords):  
                queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+' '#+'\n\n'+r'</top>'+'\n\n'
            for expansionWordIndex in range(lengthExpansionWords):
                queryExpansionContent += expansionWordsSelect[str(queryId)][expansionWordIndex] + ' '
            queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
        #print queryExpansionContent
    elif hasWeight=='yes':
        for queryId in range(1,len(originalWords)+1):
            queryExpansionContent += '<top>\n\n'+'<num> Number: '+str(queryId)+'\n\n'+'<desc>\n\n'
            lengthOrigialWords = len(originalWords[str(queryId)])
            lengthExpansionWords = len(expansionWordsSelect[str(queryId)])
            for originalWordIndex in range(lengthOrigialWords):  
                queryExpansionContent += originalWords[str(queryId)][originalWordIndex]+'^'+str(1-weightExpansionWords)+' '#+'\n\n'+r'</top>'+'\n\n'
            for expansionWordDictListIndex in range(lengthExpansionWords):
                expansionWordDict = expansionWordsSelect[str(queryId)][expansionWordDictListIndex]
                lengthExpansionWordDict = len(expansionWordDict)
                for expansionWord in expansionWordDict:
                    expansionWordTermList = expansionWord.strip().split(' ')
                    #lengthExpansionWordTermList = len(expansionWordTermList)
                    for expansionWordTerm in expansionWordTermList:
                        queryExpansionContent += expansionWordTerm +'^'+str(weightExpansionWords/lengthExpansionWordDict)+' '
            queryExpansionContent += '\n\n'+r'</top>'+'\n\n'
    support.saveFile(queryExpansionContent.replace('xray', 'x-ray'), combineQueryFile)
    return 0

if __name__ == "__main__":  
    originalWords = support.extractOriginalWords('I:\\bibm2016\\experiments\\cds2016\\query\\2016OriginalQuery.txt')
    meshExpansionWordsDict = meshExpansion(originalWords, 'all')
    #for expansionWeight in range(1,10):
     #   combineExpansionOriginalWordsWeightSame(originalWords, meshExpansionWordsDict, 'yes', expansionWeight*1.0/10, 
      #                                          'I:\\bibm2016\\experiments\\cds2014\\query\\final3\\meshSynonym\\2014MeshExpansion_'+str(expansionWeight)+'.query')
    combineExpansionOriginalWordsWeightSame(originalWords, meshExpansionWordsDict, 'yes', 0.5, 
                                                'I:\\bibm2016\\experiments\\cds2016\\query\\final3\\meshSynonym\\2016MeshSynonymExpansion_05.query')
    
   