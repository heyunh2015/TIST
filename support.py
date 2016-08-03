import os 
SystemPathSeperator = '\\'

def saveFile(string, fileName):
    fp_w = open(fileName,'w')
    fp_w.write(string)        
    fp_w.close()
    return 0

def listDir(path):
    list = []
    for file in os.listdir(path):  
        if os.path.isdir(os.path.join(path, file)):  # dir 
            list.extend(listDir(os.path.join(path, file)))
        else:  # file
            list.append(os.path.join(path, file))
    return list

def sampleEvalOnFolder(evaluateTool, qrelFile, resultFiles, evalFiles):
    files = listDir(resultFiles)
    
    for file in files:
        filename = file[file.rfind(SystemPathSeperator) + 1:]
        cmdStr = evaluateTool + SystemPathSeperator + 'sample_eval.pl -q ' + qrelFile + ' ' + resultFiles + SystemPathSeperator + filename + ' > ' + evalFiles + SystemPathSeperator + filename + '.eval'
        print cmdStr
        ret = os.popen(cmdStr).read().strip()
    return 0