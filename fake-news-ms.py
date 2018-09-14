# @author Ko, Ivan

"""Iterate through a csv file, parse the title, and generate a list with each Word containing the strTemp\
and its occurance as count. Then sort the list in descending other for count. Next, using the input value n to \
find the count of the nth node in the list, get the count value associated that that node as k, then \
print out all nodes that has count values large than or equal to k."""


import csv
import sys
import string

INDEX_TITLE = 4

class Word:
    """Necessary attributes. The comparison is for the ._word attribute."""
    def __init__(self, strTemp):
        self._word = strTemp
        self._count = 1
    
    def word(self):
        return self._word
    
    def count(self):
        return self._count
    
    def incr(self):
        self._count += 1
        
    def __eq__(self, other):
        return self._word == other._word
    
    def __lt__(self, other):
        return self._word < other._word
    
    def __le__(self, other):
        return self._word <= other._word    
    
    def __gt__(self, other):
        return self._word > other._word    
    
    def __ge__(self, other):
        return self._word >= other._word        
    
    def __str__(self):
        return (self._word + " : " + str(self._count))
    
    def __repr__(self):
        return (self._word + " : " + str(self._count))


def merge(list1, list2):
    """Merge two lists by their word count."""
    if list1 == [] or list2 == []:
        return list1 + list2
    
    else:
        if list1[0].count() > list2[0].count():
            return ([list1[0]] + merge(list1[1:], list2))
        else:
            return ([list2[0]] + merge(list1, list2[1:]))

def msort(listIn):
    """Recursively split a list into two lists, and then sort by their word count."""
    if len(listIn) <= 1:
        return listIn
    
    mid_pt = len(listIn)//2
    list1 = listIn[ :mid_pt]
    list2 = listIn[mid_pt: ]
    sortedList1 = msort(list1)
    sortedList2 = msort(list2)
    return merge(sortedList1, sortedList2)

def mergeWords(list1, list2):
    if list1 == [] or list2 == []:
        return list1 + list2
    
    else:
        if list1[0].word() < list2[0].word():
            return ([list1[0]] + mergeWords(list1[1:], list2))
        else:
            return ([list2[0]] + mergeWords(list1, list2[1:]))    


def msortbyAlphabet(listIn):
    """Does NOT WORK! Reached max recursion. The sort will be handle by default sort() using arg key=lambda."""
    if len(listIn) <= 1:
        return listIn
    print(listIn)
    split_pt = len(listIn)
    for i in range(0, len(listIn)-1, -1):
        if listIn[i].count() != listIn[i-1].count():
            if len(listIn) >= 2:
                split_pt = i-1-1

            print("split_pt is ", listIn[split_pt], split_pt)
            break
        
    list1 = listIn[ :split_pt]
    list2 = listIn[split_pt: ]
    sortedList1 = msortbyAlphabet(list1)
    sortedList2 = msortbyAlphabet(list2)
    return mergeWords(sortedList1, sortedList2)        

def main():
    
    fileName = input("File: ") #"in100.csv" #input("File: ")
    
    try:
        inFile = open(fileName)
    except OSError:
        print("ERROR: Could not open file " + fileName)
        sys.exit(1)
    
    csvReader = csv.reader(inFile)
    
    listWords = []
    
    try:
        n = int(input("N: ")) #10 #int(input("N: "))
    except (ValueError, TypeError):
        print("ERROR: Could not read N")
        sys.exit(1)
    
    assert (n >= 0)
    
    
    #count = 0 #this count is for checking if parsing is correct, in this case it's using trump. See the if trump in strTemp case.
    for line in csvReader:
        if "#" in line[0]:
            continue
        listTemp = []
        #NOTE: Need to add these three special rules so that it'd count people correctly. Sometimes things like "post-trump" or \
        #"Hillary's" didn't get counted (instead of "post" "trump", it's "posttrump"; instead of "hillary" and "s", it's "hillarys", \
        #same for "100percent.com" which should be treated as "100percent" and "com"
        line[INDEX_TITLE] = line[INDEX_TITLE].replace("'", " ")
        line[INDEX_TITLE] = line[INDEX_TITLE].replace("-", " ")
        line[INDEX_TITLE] = line[INDEX_TITLE].replace(".com", " com")
        #Split the space, which is why I replaced those characters with spaces.
        listTemp = line[INDEX_TITLE].split()

        #print(listTemp)
        
        for strTemp in listTemp:
            #print(strTemp)
            strTemp = strTemp.translate(strTemp.maketrans("", "", string.punctuation)).lower()
            strTemp = strTemp.translate(strTemp.maketrans("", "", string.whitespace))
            
            
            if len(strTemp) > 2:
                #Only count/add words longer than 2 characters.
                #print(strTemp)
                temp = Word(strTemp)
                
                #if "trump" in strTemp:
                    #count += 1
                    #print("\n\n---TRUMP ", ": ", count, "| strTemp was ", strTemp)
                
                if temp not in listWords:
                    #print("adding new word - ", temp)
                    listWords.append(temp)
                else:
                    #print("found word - ", temp, " - increment value")
                    listWords[listWords.index(temp)].incr()
        #print(listWords)
            
    inFile.close() 
    
    #print(listWords)
    
    sortedListWords = msort(listWords)
    
    #print(sortedListWords)
    
    minCount = sortedListWords[n].count()
    #print(minCount)
    
    relevantList = [x for x in sortedListWords if x.count() >= minCount]
    #print("relevant list\n", relevantList)
    #NOTE: sort by value first, and then the alphabet
    relevantList.sort(key=lambda x:(-x.count(), x.word()))
    #print("relevant list after alphabet sort\n", relevantList)
    for i in relevantList:
        print(i)


"""--------------------------------------------------
-------------------------------------------------------
-----------------------------------------------------"""



def mergeTest(list1, list2):
    if list1 == [] or list2 == []:
        return list1 + list2
    
    else:
        if list1[0] > list2[0]:
            return ([list1[0]] + mergeTest(list1[1:], list2))
        else:
            return ([list2[0]] + mergeTest(list1, list2[1:]))

def msortTest(listIn):
    if len(listIn) <= 1:
        return listIn
    
    mid_pt = len(listIn)//2
    list1 = listIn[ :mid_pt]
    list2 = listIn[mid_pt: ]
    sortedList1 = msortTest(list1)
    sortedList2 = msortTest(list2)
    return mergeTest(sortedList1, sortedList2)



def test():  
    listTest = []
    print(listTest)
    
    word01 = Word("may")
    word02 = Word("yam")
    word03 = Word("hey")
    word04 = Word("huun")
    word05 = Word("huur")
    word06 = Word("tu")
    
    if word01 in listTest:
        print("yes ", word01)
    else:
        print("no ", word01)
    
    listTest.append(word01)
    print(listTest)
    
    
    print(listTest[listTest.index(word01)])
    listTest[listTest.index(word01)].incr()
    print(listTest[listTest.index(word01)])
    
    if word01 in listTest:
        print("yes ", word01)
    else:
        print("no ", word01)    
        
    word01 = Word("okay?")
    
    if word01 in listTest:
        print("yes ", word01)
    else:
        print("no ", word01)    
        listTest.append(word01)
    
    word01 = Word("may")
    
    if word01 in listTest:
        print("yes ", word01, "incrmenting...")
        listTest[listTest.index(word01)].incr()
        print("updated: ", listTest[listTest.index(word01)])
    else:
        print("no ", word01)    
        listTest.append(word01)    
    
    print(listTest)    
    
    print("\n\ntesting merge")
    L01 = [11, 22, 33]
    L02 = [5, 10, 15, 20, 25]
    print("L02[:-1] ", L02[:-1])
    
    L03 = mergeTest(L01, L02)
    print(L03)
    
    print("testing msort")
    L04 = [3, 1, 0]
    L05 = [4, 2, 9, 5]
    L6 = msortTest(mergeTest(L04, L05))
    print(L6)
    
    print("\n\ntseting str comparision")
    str01 = "apple"
    str02 = "ace"
    
    if str01 > str02:
        print("str01 larger")
    else:
        print("str02 larger")
    
    listStr = [str01, str02]
    listStr.sort(key=str.lower)
    print(listStr)
    
    print("\ntesting alphabetic sort")
    listTest.append(word03)
    print("before: ", listTest)
    
    #listTest.sort(key=lambda x: x.word())
    #print("after: ", listTest)
    
    #listTest = msortbyAlphabet(listTest)
    listTest.sort(key=lambda x:(-x.count(), x.word()))
    
    print(listTest)
    
main()
#test()
