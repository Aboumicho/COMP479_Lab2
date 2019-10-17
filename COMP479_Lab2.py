import os
from os import path
import re
from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
import sys
import codecs

class Spimi:

    def __init__(self):
        self.directory = os.getcwd()
        self.cpt = sum([len(files) for r, d, files in os.walk(str(self.directory)+"/reuters")])
        self.disk = "DISK"
        self.pathDisk = self.directory+ "/" + self.disk 
        self.pathReuters = self.directory +'/reuters'
        self.size = 0
        self.sizeDISK = 0
        self.Hash = []
        self.HashSize = 0
        self.pathCurrentBlock = ""

    #Get all reuters tags from all files
    def search(self):
        #get number of files
        directory = self.directory
        cpt = self.cpt
        for i in range(cpt):
            #Search for all reuters articles
            file_name = 'reut2-' + str(f'{i:03}') + '.sgm'
            reuters_file = open(directory + "/reuters/" + file_name).read()
            file_table = file_name.split(".")[0] + "_table.txt"
            if path.exists(file_table):
                print(file_table + " already exists in directory!")
            else:    
                soup = BeautifulSoup(reuters_file, 'html.parser')
                reuters_tag = soup.find_all('reuters')

                all_places = open('all-places-strings.lc.txt').read()
                list_places = []
                #loop through articles 
                for reuter in reuters_tag:
                    article_id = reuter.get('newid')
                    row = "Article newid="+str(article_id) + ": " 
                    #check for places in reuter article
                    for place in all_places.split("\n"):
                        if place in reuter.get_text():
                            row += place + " | "
                    #write to file
                    row += "\n"
                    table = open(file_table, "a")
                    table.write(row)

    def createStorage(self):
        if not os.path.isdir(self.directory):
            os.mkdir(self.disk)

    def getSizeDISK(self):
        file_name = 'temp.txt'
        if not os.path.isfile(self.directory + "/" + file_name):
            file_name = 'reut2-' + str(f'{0:03}') + '.sgm'
            reuters_file = open(self.pathReuters + "/" + file_name).read()
            soup = BeautifulSoup(reuters_file, 'html.parser')
            reuters_tag = soup.find_all('reuters')
            file_write = open(file_name, "a")
            #Get size of 500 reuters articles
            for i in range(500):
                file_write.write(reuters_tag[0].get_text())
            os.path.getsize(self.directory + "/" + file_name)
            self.sizeDISK = os.path.getsize(self.directory + "/" + file_name)
            return self.sizeDISK
        else:
            os.path.getsize(self.directory + "/" + file_name)
            self.sizeDISK = os.path.getsize(self.directory + "/" + file_name)
            return self.sizeDISK

    def memoryUsedInDisk(self):
        for filename in os.listdir(self.directory+ "/" + self.disk):
            self.size += os.path.getsize(self.pathDisk + "/" + filename)

    #Big funtion creating dictionary
    def createDictionary(self):
        doesDictionnaryExist = False
        listAllBlocks = sum([len(files) for r, d, files in os.walk(str(self.pathDisk))])
        for i in range(len(listAllBlocks)):
            if os.path.isfile(self.pathDisk + "/block" + str(i) + "/block" + str(i) + ".txt"):
                doesDictionnaryExist = True
                break
        if not doesDictionnaryExist:        
            directory = self.directory
            cpt = self.cpt
            tokenslist = []
            #loops through reuters articles
            #for i in range(cpt)
            for i in range(cpt):
                #Search for all reuters articles
                file_name = 'reut2-' + str(f'{i:03}') + '.sgm'
                reuters_file = open(directory + "/reuters/" + file_name).read()
                soup = BeautifulSoup(reuters_file, 'html.parser')
                reuters_tag = soup.find_all('reuters')
                self.pathCurrentBlock = self.pathDisk +"/BLOCK" + str(i)
                for reuter in reuters_tag:
                    tokenl = nltk.word_tokenize(reuter.get_text()) 
                    self.listTerms(tokenl, reuter.get('newid'))
                #     break
                # break
    
    #List tokens of 1 article with its docID and Frequency
    def listTerms(self, tokenList, article_id):
        sorted_list = sorted(tokenList)
        dictionnary = []
        count = 0
        index = 0
        term = ""
        if sys.getsizeof(self.Hash) >= self.getSizeDISK():
            self.mergeBlocks()
        if sys.getsizeof(self.Hash) <= self.getSizeDISK():                   
            for token in sorted_list:
                t = token.replace('\\', '/')
                #base case
                if index == 0:
                    term = t
                index += 1
                if (not any(t in i for i in dictionnary)):               
                    if t == term :
                        count += 1
                    else: 
                        dictionnary.append((term, article_id, count))    
                        count = 1
                        term = t
        
        self.Hash.append(dictionnary) 

    def mergeBlocks(self):
        temp = [None] * round((len(self.Hash) / 2))
        j = 0
        while len(self.Hash) > 2:
            for i in range(len(self.Hash)):
                if(i % 2 == 1 ):
                    temp[j] = self.Hash[i] + self.Hash[i-1]
                    print("Merge Block " + str(i-1) + " with Block " + str(i) + " to new index " + str(j))
                    j+=1
            self.Hash = temp
            temp = [None] * round((len(self.Hash) / 2))
            j = 0
        for i in range(len(self.Hash)):
            temp = sorted(self.Hash[i])
            self.Hash[i] = temp

    def writeBlockToDisk(self):
        for i in range(len(self.Hash)):
            #Case Block exists
            if os.path.isdir(self.pathDisk + "/block" + str(i)):
                #If Block file already exists
                if os.path.isfile(self.pathDisk + "/block" + str(i) + "/block" + str(i) + ".txt"):
                    print("Writing to block " + str(i) + " interrupted. Dictionary exists already.")
                #Create and write to block file
                else:
                    block = codecs.open((self.pathDisk + "/block" + str(i) + "/block" + str(i) + ".txt"), "a", encoding='utf-8')
                    block.write("term                    docID                    frequency")
                    for key, value, frequency in self.Hash[i]:
                        if key != " " or key!=None or key != "": 
                            #print(key + "          " + str(value) + "          " + str(frequency))
                            block.write(key + "                    " + str(value) + "                    " + str(frequency))
            #case Block does not exists
            if not os.path.isdir(self.pathDisk + "/block" + str(i)):
                os.mkdir(self.pathDisk + "/block" + str(i))
                #If Block file already exist
                if os.path.isfile(self.pathDisk + "/block" + str(i) + "/block" + str(i) + ".txt"):
                    print("Writing to block " + str(i) + " interrupted. Dictionary exists already.")
                #Create file
                else:
                    block = codecs.open((self.pathDisk + "/block" + str(i) + "/block" + str(i) + ".txt" ), "a", encoding='utf-8')
                    block.write("term                    docID                    frequency \n")
                    for key, value, frequency in self.Hash[i]:
                        if key != " " or key!=None or key != "": 
                        #print(key + "          " + str(value) + "          " + str(frequency))
                            block.write(key + "                    " + str(value) + "                    " + str(frequency) + "\n")

    #def loadDictionnary(self):
        
test = Spimi()
test.createStorage()
test.getSizeDISK()
test.memoryUsedInDisk()
test.createDictionary()
test.mergeBlocks()
test.writeBlockToDisk()
#print(test.Hash[4999])
#print(test.HashSize)
# print(sys.getsizeof( test.Hash))
# print(test.Hash[0])
