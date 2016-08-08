#! /usr/bin/python
# -*- coding: utf-8 -*- 
import os

def listDir(path):
    list = []
    for file in os.listdir(path):  
        if os.path.isdir(os.path.join(path, file)):  # dir 
            list.extend(listDir(os.path.join(path, file)))
        else:  # file
            list.append(os.path.join(path, file))
    return list

def getDocumentLength(fileName):
    fp = open(fileName)
    text = fp.read()
    wordList = text.strip().split(' ')
    length = 0
    for word in wordList:
        if word!='':
            length+=1
    return length

def getCollectionAverageLength(folderName):
    fileList = listDir(folderName)
    lengthCount = 0
    for fileName in fileList:
        length = getDocumentLength(fileName)
        lengthCount += length
    
    return lengthCount*1.0/len(fileList)

if __name__=='__main__':     
    #print getDocumentLength('C:\\Users\\hy\\Desktop\\1064073.nxml')
    print getCollectionAverageLength('/home/lmy/trec16/raw_data_preprocess/pmc-00/00')