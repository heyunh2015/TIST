#coding=utf-8
'''
Created on 2015年9月4日

@author: Administrator
'''

import os
import numpy as np
from scipy.stats import  wilcoxon
import support


#from ResultParse.EvalParse import evalMapParse, evalP30Parse

PATH_SPLIT = os.sep

#===============================================================================
# The Wilcoxon signed-rank test tests the null hypothesis that two related paired samples 
# come from the same distribution. In particular, it tests whether the distribution of the 
# differences post - pre is symmetric about zero. It is a non-parametric version of the paired T-test.
#===============================================================================
def wilcoxonSignedRankTest(pre, post):
    (z_statistic, p_value) = wilcoxon(post - pre)
    # if p_value < 0.05 , the difference in mean is not equal to 0(post has a significant improvement over pre)
    #print "paired wilcoxon-test, p: ", p_value
    return (z_statistic, p_value)


def significanceTest(preFilePath, postFilePath, matric):
    preMatricList = extractEvalValue(preFilePath, matric)
    postMatricList = extractEvalValue(postFilePath, matric)
 
    pre = np.array(preMatricList)
    post = np.array(postMatricList)
    #print (post - pre)[22]
    #print (post - pre)[28]
    #print (post - pre)[29]
    
    (z_statistic, p_value) = wilcoxonSignedRankTest(pre, post)
    return (z_statistic, p_value)


def generatePairs(year, model):
    pairs = list()
    if model == 'LM':
        fileDir = '../data/eval/' + year + '/selected/' + model + '/'
        files = ['myLM.txt', 'myLM_dRecency.txt', 'myLM_dKDE_prf50.txt',\
                 'myLM_dRecency-myLM_qKDE_dRecency_prf50.txt', 'myLM-myLM_dKDE-myLM_qKDE.txt']
        pairs.append([fileDir + files[1], fileDir + files[0]])
        pairs.append([fileDir + files[2], fileDir + files[0]])
        pairs.append([fileDir + files[2], fileDir + files[1]])
        pairs.append([fileDir + files[3], fileDir + files[0]])
        pairs.append([fileDir + files[3], fileDir + files[1]])
        pairs.append([ fileDir + files[3], fileDir + files[2]])
        pairs.append([fileDir + files[4], fileDir + files[0]])
        pairs.append([fileDir + files[4], fileDir + files[1]])
        pairs.append([ fileDir + files[4], fileDir + files[2]])
        
    elif model == 'LM_PRF':
        fileDir = '../data/eval/' + year + '/selected/' + model + '/'
        files = ['LM_prf.txt', 'LM_prf-LM_dRecency.txt', 'LM_prf-LM_dKDE.txt',\
                 'LM_prf-LM_qKDE_dRecency.txt', 'LM_prf-LM_dKDE-LM_qKDE.txt']
        pairs.append([fileDir + files[1], fileDir + files[0]])
        pairs.append([fileDir + files[2], fileDir + files[0]])
        pairs.append([fileDir + files[2], fileDir + files[1]])
        pairs.append([fileDir + files[3], fileDir + files[0]])
        pairs.append([fileDir + files[3], fileDir + files[1]])
        pairs.append([ fileDir + files[3], fileDir + files[2]])
        pairs.append([fileDir + files[4], fileDir + files[0]])
        pairs.append([fileDir + files[4], fileDir + files[1]])
        pairs.append([ fileDir + files[4], fileDir + files[2]])
        
    return pairs
        
        
def extractEvalValue(fileName, matric):
    matricList = []
    fp = open(fileName)
    for line in fp.readlines():
        lineArr = line.strip().split('\t\t')
        if lineArr[0]==matric and lineArr[1]!='all':
            matricList.append(float(lineArr[2]))
    #print matricList
    return matricList       
                    
        
        

if __name__=='__main__':                                      
    #(z_statistic, p_value) = significanceTest('I:\\bibm2016\\experiments\\cds2014\\eval\\final\\BM25b0.75_1908.res.eval',
     #                                         'I:\\bibm2016\\experiments\\cds2014\\eval\\final\\BM25b0.75_1911.res.eval',
      #                                        'infNDCG')       
    #print (z_statistic, p_value)
    fileList = support.getResultFileNameFromFile('I:\\bibm2016\\experiments\\cds2015\\eval\\final3', 
                                                'H:\\Users2016\\hy\\workspace\\bibm2016\\significanceTest\\testFile.txt')
    
    for preFileIndex in range(0, len(fileList)):
        for postFileIndex in range(preFileIndex+1, len(fileList)):
            (z_statistic, p_value) = significanceTest(fileList[preFileIndex]+'.eval',
                                                      fileList[postFileIndex]+'.eval',
                                                      'infNDCG')
            if p_value<0.05:
                print fileList[preFileIndex], fileList[postFileIndex], p_value
    
    #resultList = extractEvalValue('I:\\bibm2016\\experiments\\cds2015\\eval\\final2\\BM25b0.75_696.res.eval', 'iP10')
    #print resultList[12]
    #print resultList[25]
    #print resultList[26]
    #print resultList[28]
  
        
        
        
        
        
        
        
        
        