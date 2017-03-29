# -*- coding: utf-8 -*- 
import support as support
import re
from bs4 import BeautifulSoup

def extractTagContent(originalQueryFile, tagName):
    soup = BeautifulSoup(open(originalQueryFile))
    #print soup.prettify()#格式化输出对象内容
    for tagObject in soup.find_all(tagName):#找到所有指定节点
        print tagObject.string
    return soup.find_all(tagName)

def removePunctuation(text):
    r='[��!"#$%&\'()*+,.��/:;<=>?@[\\]^_`{|}~]+'
    text = re.sub(r,'',text)
    text = re.sub('  ',' ',text)
    #text = re.sub('-',' ',text)
    #text = re.sub('—',' ',text)
    text = re.sub('·','',text)
    text = re.sub('•','',text)
    return text

def saveCDSidFile(tagObjetcList, queryForGoogleFile):
    CDSidFileTxt = ''
    queryId = 1
    for tagObject in tagObjetcList:#找到所有指定节点
        CDSidFileTxt += str(queryId) + '\t' + removePunctuation(tagObject.string.strip()) + '\n'
        queryId += 1
    support.saveFile(CDSidFileTxt, queryForGoogleFile)
    return 0

def saveTerrierFile(tagObjetcList, queryForTerrier):
    TerrierFileTxt = ''
    queryId = 1
    for tagObject in tagObjetcList:#找到所有指定节点
        TerrierFileTxt += '<top>'+'\n'+'<num> '+'Number: '+str(queryId)+'\n'+\
         '<desc>'+'\n' + removePunctuation(tagObject.string.strip()) + '\n' + '</top>'+'\n'
        queryId += 1
    support.saveFile(TerrierFileTxt, queryForTerrier)
    return 0

if __name__ == "__main__": 
    tagObjetcList = extractTagContent('I:\\trec2016\\query\\16topics.txt', 'summary')
    #saveCDSidFile(tagObjetcList, 'I:\\bibm2016\\experiments\\GoogleSearch\\data\\2016.CDSid_queryOriginal.txt')
    saveTerrierFile(tagObjetcList, 'I:\\bibm2016\\experiments\\cds2016\\query\\2016OriginalQuery.txt')