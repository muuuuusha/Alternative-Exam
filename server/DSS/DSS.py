import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize as wt

import sqlite3
import pandas as pd
import numpy as np
import sys


lemmatize = WordNetLemmatizer().lemmatize

def clearFromTrash(text):
    for i in range(len(text)):
        for j in range(len(text[i])):
            if text[i][j] in ('.', ',', '(', ')', '{', '}', '[', ']', '/', ';', '$'):
                text[i][j].replace(text[i][j], '')
    return text

def lemmatizeText(text):
    lemmed = []
    for i in range(0, len(text)):
        if text[i].lower() not in ('$', 'at', 'to', 'on', 'with', "in", 'we', 'i', 'their', 'that', 'this', 'are', 'by', 'an', 'as', 'such', 'to', 'of', 'the', 'a', 'is', 'and', '.', ',', '(', ')', '{', '}', '[', ']', '/', ';') and text[i] not in lemmed:
            lemmed.append(lemmatize(text[i].lower()))
    return lemmed

def calculateWeight(lemmed1, lemmed2):
    weight = 0
    for i in lemmed1:
        if i in lemmed2:
            weight += 1
    return weight

def getWeightMatrix(clearedTexts: np.array) -> np.ndarray:
    length = len(clearedTexts)
    weightMatrix = np.zeros((length, length), dtype=int)
    
    for i in range(length):
        for j in range(i, length):
            if (i == j):
                weightMatrix[i][j] = 0
                continue
            weightMatrix[i][j] = calculateWeight(clearedTexts[i], clearedTexts[j])
            weightMatrix[j][i] = weightMatrix[i][j]    
    
    return weightMatrix

def loadMatrix(path):
    return np.loadtxt(path, delimiter=',', dtype=int)

def main(DBPath, articlesCount):
    conn = sqlite3.connect(DBPath)
    c = conn.cursor()
    
    
    c.execute("SELECT id, content FROM articles")
    data = c.fetchall()
    
    dataFrame = pd.DataFrame(data, columns=['id', 'content'])
    data = dataFrame['content'].values
    
    if articlesCount:
        data = data[:articlesCount]
    data = [clearFromTrash(i) for i in data]
    data = np.array([lemmatizeText(wt(i)) for i in data], dtype=object)
    
    
    weightMatrix = getWeightMatrix(data)
    
    conn.close()
    return weightMatrix

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python DSS.py <.sqlite3> <.txt> [articles count]")
        sys.exit(1)
        
    if len(sys.argv) == 4:
        if sys.argv[3].isdigit():
            articlesCount = int(sys.argv[3])
        elif sys.argv[3] == "all":
            articlesCount = None
    else:
        articlesCount = 100
        
    import time
    start = time.time()
    print("Calculating weight matrix...")
    weightMatrix = main(sys.argv[1], articlesCount)
    print("Time spent: ", time.time() - start)

    # save weight matrix to file
    np.savetxt(sys.argv[2], weightMatrix, delimiter=',', fmt='%d')