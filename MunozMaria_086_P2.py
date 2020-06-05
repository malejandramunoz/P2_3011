"""This program reads DNA sequences from an input file and finds the
consensus sequence.  An output file is also created to store the
counts per column, so as to validate the consensus.
Add the corresponding code to accomplish the requested tasks
"""



##### INFORMATION #######
# NAME: Maria Alejandra Munoz Valenzuela
# STUDENT ID: 802-18-8690
# SECTION: 086
###########################################################


def load_data(fileName):
    """"Reads DNA sequences from file and return them in a list."""
    foriginal = open(fileName)  # this assumes the file will exist and will not check for it, if the file doesn't exist,
    # it will have a traceback
    dataList = list()  # creates the empty list that i will use to append the sequences.
    for line in foriginal:
        line = line.strip()  # makes sure that the line doesn't have any special characters
        if not line.startswith('>'):  # checks the lines to see if they don't start with >
            dataList.append(line)  # if the line starts with anything but a >, it's saved to the list of data to be
            # processed
    foriginal.close()  # it closes the file as i will not be using it again
    return dataList  # returns it to be used in another function.


def count_nucl_freq(dataList):
    """Count the occurrences of characters by column."""
    pos = 0  # it's a counter to make sure it's the correct position every time
    resultList = list()  # creates an empty list to append the things
    while len(resultList) != len(dataList[0]):  # it makes sure that this result list is not bigger than the length
        # of the strings in dataList
        insideString = ""  # this is inside the while, so that every time it finishes and goes to top, it's a "new" list
        for value in dataList: # it does it for every value inside the dataList
            insideString = insideString + value[int(pos)]  # the inside string is the columns
        resultList.append(insideString)  # it appends the columns so that once it's lists is "renovated", i can
        # still reference it
        pos += 1  # an update counter

    alphabetlist = list()  # the list of letters in the resultingList, which is what would we use to find each count
    for listings in resultList:  # it enters the list and shows every list of columns
        for chars in listings:  # it enters every character of the columns
            if chars not in alphabetlist:  # it checks if it's not in the character so it can be added.
                alphabetlist.append(chars)  # it appends the character, so that it can be turned into a dictionary later

    def alphabet_dictionary(alphabetlist):  # this is a function that will be used more than once during this specific
        # function
        alphabetdictionary = dict() # it opens the dictionary that i want use
        for letters in alphabetlist:  # it goes inside the list that i already have, so it can take each value
            alphabetdictionary[letters] = alphabetdictionary.get(letters, 0)  # as i am not counting yet, i put the
            # value at 0
        return alphabetdictionary

    countStruct = list()  # finally this is the list that i will return in this function
    for eachString in resultList:  # it goes inside each string in the result List, which are the columns
        countDictionary = alphabet_dictionary(alphabetlist)  # it creates the dictionary every time so it's a "new" one
        for eachCharacters in eachString:  # now it starts counting
            countDictionary[eachCharacters] = countDictionary[eachCharacters] + 1
        countStruct.append(countDictionary)  # it appends the dictionary into the list that will be returned
    return countStruct
    

def find_consensus(countData):
    """Returns the consensus sequence according to highest-occuring nucleotides"""

    resultingList = list() # empty list to be used in the for
    for dictionary in countData:  # it goes inside the each dictionary in countData
        changingdictionary = list()  # it updates the dictionary every time it does an iteration so that it's a "new"
        # dictionary
        for key, value in dictionary.items():  # it takes each key and value, reverses them and then sorts them from
            # biggest to smallest
            changingdictionary.append((value, key))
            changingdictionary = sorted(changingdictionary, reverse=True)
        resultingList.append(changingdictionary)  # it appends the newly turned tuple into a list to be used letter

    consensusString = ""  # empty string to be returned
    counter = 0 # this counter is to print the correct position
    for lists in resultingList:  # this goes inside each list so it can take what i need from each one of them
        letter = resultingList[counter][0][1]
        consensusString += letter  # adds the letter to the string
        counter += 1  # updates the counter
    return consensusString


def process_results(countData, outFilename):
    """Prints consensus to screen and stores results in output file."""
    consensus = find_consensus(countData)  # gives me the string found before so it can print it
    print(consensus)
    resultingList = list()  # empty lists, same method used before
    for dictionary in countData:  # as countData is given to me in disorder i have to put it in order once more, doing
        # the same as before except i don't find the string
        changingdictionary = list()
        for key, value in dictionary.items():
            changingdictionary.append((value, key))
            changingdictionary = sorted(changingdictionary, reverse=True)
        resultingList.append(changingdictionary)

    position = 1  # this is what gives the count to save the positions in the file
    fnew = open(outFilename, "w")  # opens the new file
    fnew.write("Consensus: ",)
    fnew.write(consensus)
    fnew.write("\n")
    for elements in resultingList:  # it begins to loop for each consensus that were organized
        if position < 10:  # this if/else is used to make sure that they all look the same when saved to the file
            fnew.write("Pos",)
            fnew.write(" ")
            fnew.write(str(position))
            fnew.write(": \t\t",)
        else:
            fnew.write("Pos",)
            fnew.write(" ")
            fnew.write(str(position))
            fnew.write(":\t\t", )
        for tuples in elements:  # now it goes inside the tuples that are inside of it
            consensusList = list()  # it creates this new list that will be updated so it's a "new" list
            for count in tuples:  # goes inside each tuple to take out the value
                tobesaved = count  # this is a temporary variable to be put in the new list so that it can written into
                #  the file
                consensusList.insert(0, tobesaved)  # this puts the last thing inside the tuple first, which it what i
                # want to do
            fnew.write(consensusList[0])  # this prints the letter which is the last in the tuple
            fnew.write(":")
            fnew.write(str(consensusList[1]))  # this prints the letter which is the first in the tuple in the tuple
            fnew.write("\t")  # makes sure that the spaces are even

        position += 1  # updates the position count so it can be in the correct order
        fnew.write("\n")  # makes a new line


def main():

    # File name "constants". Assume the names of the files don change.
    INPUTFILE  = "DNAInput.fasta"
    OUTPUTFILE = "DNAOutput.txt"

    seqList = load_data(INPUTFILE)

    countData = count_nucl_freq(seqList)

    process_results(countData, OUTPUTFILE)

# The code below makes Python start from the main function
# whenever our program is invoked as a "standalone program"
# (as opposed to being imported as a module).
if __name__ == "__main__":
    main()
