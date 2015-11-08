"""
Source Code from
    http://stackoverflow.com/questions/8286554/find-anagrams-for-a-list-of-words

- Modified:
    Add comments explaining code.
    Add add a word counter.
    better entry point.
    Add graphing of histograms
    Added SQL portion    
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import time

#Create our table to hold the anagrams
def CreateAnagramTable():
    c.execute("DROP TABLE IF EXISTS anagrams;") #allows for rerunning :)   
    c.execute("""
    CREATE TABLE anagrams (
    UniqueAnagramID varchar(20) NOT NULL,
    numberWords int NOT NULL,
    WordList varchar(500) NOT NULL) 
    """)
    conn.commit()

#take a list of values, and insert them all into DB
#  Would be better to pass in a tuple(s) and execute many
#  but it's late and I'm working record by record
def InsertRecord(uniqueid,numWord,listWord):
    query ="insert into anagrams values ('%s',%s,'%s')" \
         % (uniqueid, str(numWord), listWord)
    
    print query  # for debugging 
    c.execute(query)
    conn.commit()
    time.sleep(.25)
    
    #preferred method, not what I did.
    #c.executemany("insert anagrams values (?,?,?)",tupleOfAnagrams)

# just to see whats in there...
def SelectAllFromDB():
    for row in c.execute("select * from anagrams"):
        print row
        
def GetNumberAnagrams():
    c.execute("select count(*) from anagrams")
    print c.fetchone()


#########################################
# Below here is the same solution as q1-3
# with the DB stuff added.
#########################################

#This function reads the source file
#For each word, it removes whitespace and junk.
def load_words(filename='c:/temp/ospd.txt'):
    with open(filename) as f:
        for word in f:
            yield word.rstrip()

# For each word in the loaded words, create a new dictionary entry for it.
# return the dictionary of all words, with the original word as the key, and 
# the value all letters in the word, sorted.
def get_anagrams(source):
    
    d = defaultdict(list)
    for word in source:
        key = "".join(sorted(word))
        d[key].append(word)
    return d

# Go through the dictionary of all words. 
# the dictionary is sorted
# compare the "key" word (word being looked up) to all items 
# in the anagram list.  If they are the same length, then they are an anagram.
def print_anagrams(word_source):
    d = get_anagrams(word_source)
    counter = 0
    highcount=0
    highcountwords = ""
    histogramDict = defaultdict(int)

    for key, anagrams in d.iteritems():
        length = len(anagrams)
                
        if length > 1:
            print(key,anagrams)
            counter += 1
            histogramDict[str(length)]+=1 #add count to histogram            

            #see if this word has the most anagrams so far.            
            if length > highcount:
                highcount = len(anagrams)
                highcountwords = anagrams
                print ("**********HEW HIGH COUNTER FOUND **********")

            #Add record to DB
           # InsertRecord(key,length,str(anagrams).replace("'",""))
            
    print "There are ", counter, " anagrams found."
    print "High counter is: ", highcount, highcountwords
    
    #create a bar chart.  Note the import of numpy and mtlibplot above     
    print "The histogram dictionary looks like:"
    print histogramDict.items()

    X = np.arange(len(histogramDict))
    plt.bar(X, histogramDict.values(),align='center', width=0.5)
    plt.xticks(X,histogramDict.keys())
    ymax = highcount + 7500
    plt.ylim(0, ymax)
    plt.show()
    
###########################################
# program entry point.
if __name__ == '__main__':
    # DB initilization
    conn = sqlite3.connect('hw4.db')
    c = conn.cursor()
    """ ALREADY EXISTS 
    CreateAnagramTable()
    """
    #calculate the anagrams and do the stuff for q1-3
    #word_source = load_words()
    # Alternate was to pass a word list in. 
    #word_source = ["eat","ate","tea","draper","parred", "stone", "tones", "onset", "tonse"]
    #print_anagrams(word_source)

    #SelectAllFromDB()

    print 'Question 4: How many anagrams:'
    GetNumberAnagrams()
    