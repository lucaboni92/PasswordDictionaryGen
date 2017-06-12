from random import randint
import sys

MAX_PWD_LEN = 30

def main():
    #inputfile_name = ""
    #outputfile_name = ""

    defaultMaxIterations = 10000
    defaultGeneratedResults = 50

    inputEnable = False
    outputEnable = True
    
    try:
        if len(sys.argv) > 1:
            for i in range(1,len(sys.argv)-1, 2):
                if sys.argv[i] == '-i':
                    # input from file
                    inputfile_name = sys.argv[i+1]
                    inputEnable = True
                    
                elif sys.argv[i] == '-o':
                    # output file
                    outputfile_name = sys.argv[i+1]
                    print ("---outputfile_name--->"  + outputfile_name)
                    outputEnable = False
                    
                else:
                    print ("Parameters error")
                    print ("Quitting...")
                    quit()
        
        outputSet = set()

        generatedResults = input("Number of iterations for each word [void to default]: ")
        if generatedResults != "":
            generatedResults = int(generatedResults)
        else:
            generatedResults = int(defaultGeneratedResults)

        maxIterations = defaultMaxIterations
        if generatedResults > defaultMaxIterations:
            limitCheck = input("Do want to overwrite max suggested number of iterations fixed to " + str(defaultMaxIterations) + " [y/N]? ")
            if limitCheck.lower() == "yes" or limitCheck.lower() == "y":
                maxIterations = generatedResults

        # input
        if inputEnable:
            inputSet = _readInputFile(inputfile_name)
        else:
            inputSet = _readInputKeyboard()

        # dictionary generation
        for w in inputSet:   
            i = 0
            tmpSet = set()
            while len(tmpSet) < generatedResults and i < maxIterations:
                word = w

                x = 0
                if len(inputSet) > 1:
                    x = randint(0,100)
                    
                if x < 60:
                    # operation on a single word
                    word = _lowUpCase(word)
                    word = _randCharMix(word)
                    
                elif x >= 60:
                    # operation on multiple words
                    word = _randWordMix(inputSet)

                tmpSet.add(word)
                i = i+1
            outputSet |= tmpSet

        # output
        if outputEnable:
            _printResults(outputSet)
        else:
            _printOutputFile(outputSet, outputfile_name)

        print (str(len(outputSet)) + " different combinaitons created")

    except KeyboardInterrupt:
        # to intercept CRTL+C interrupt 		
        print ("\nQuitting...")
    except ValueError:
        # conversion exception
        print ("Inserted unexpected value")
    except OSError as err:
        # file error
        print("OS error: {0}".format(err))
    except:
        # unexpected exception
        print("Unexpected error:", sys.exc_info()[0])

def _readInputFile(inputfile_name):
    inputSet = set()
    with open(inputfile_name,'r') as f:
        for line in f:
            for inputword in line.split():
               inputSet.add(inputword)   
        #text = in_file.read()
    return inputSet

def _readInputKeyboard():
    inputSet = set()
    inputword = input("Enter a word: ")
    while inputword != "":
        inputSet.add(inputword)
        inputword = input("Enter next word [void to stop]: ")
    return inputSet

def _printResults(outputSet):
    # print results on stdout
    for w in outputSet:
        print (w)

def _printOutputFile(outputSet, outputfile_name):
    # print results on file
    out_file = open(outputfile_name,"w+")
    for word in outputSet:
         out_file.write(word + "\n")
    out_file.close()

def _lowUpCase(word):
    res = []
    for c in word:
        if randint(0,100) > 50:
            if c.isupper():
                res.append(c.lower())
            elif c.islower():
                res.append(c.upper())
            else:
                res.append(c)
        else:
            res.append(c)

    return ''.join(res)

def _randCharMix(word):
    res = ""
    for i in range(0,len(word)):
        if word[i].lower() == 'a':
            if randint(0,100) > 50:
                res += '@'
            else:
                res += word[i]
                
        elif word[i].lower() == 'e':
            x = randint(0,2)
            if x == 1:
                res += '3'
            elif x == 2:
                res += '&'
            else:
                res += word[i]
                
        elif word[i].lower() == 'i':
            x = randint(0,4)
            if x == 0:
                res += word[i]
            elif x == 1:
                res += '1'
            elif x == 2:
                res += '!'
            elif x == 3:
                res += _lowUpCase("y")
            elif x == 4:
                res += _lowUpCase("j")
                
                
        elif word[i].lower() == 'g':
            if randint(0,100) > 50:
                res += '6'
            else:
                res += word[i]
                
        elif word[i].lower() == 'o':
            if randint(0,100) > 50:
                res += '0'
            else:
                res += word[i]
                
        elif word[i].lower() == 's':
            x = randint(0,2)
            if x == 1:
                res += '5'
            elif x == 2:
                res += '$'
            else:
                res += word[i]
                
        elif word[i].lower() == 'z':
            if randint(0,100) > 50:
                res += '2'
            else:
                res += word[i]
                
        else:
            res += word[i]

    return res

def _randWordMix(inputSet):
    setLen = len(inputSet)
    inputList = list(inputSet)

    # How many words to mix:
    wordNumber = randint(1, setLen)

    # Which words to mix:
    wordArray = []
    for i in range(0,wordNumber):
        index = randint(0,setLen-1)
        wordArray.append(inputList[index])

    # How many charactes has the final word:
    x = randint(0,100)
    pwdLen = 0
    if x <= 50: # 50%
        # from 4 to 8 chars
        pwdLen = randint(4,8)
    elif x > 50 and x <= 80: # 30%
        # from 9 to 16 chars
        pwdLen = randint(9,16)
    elif x > 80 and x <= 90: # 10%
        # from 0 to 3 chars
        pwdLen = randint(0,3)
    elif x > 90: # 10%
        # from 17 to MAX_PWD_LEN chars
        pwdLen = randint(17,MAX_PWD_LEN)

    word = ""
    
    # Which character use from each word:
    while len(word) < pwdLen:
        # -> select a word in the list
        aInd = randint(1,wordNumber)
        aStr = wordArray[aInd-1]
        # -> select a char in the word
        bInd = randint(1, len(aStr))
        bChar = aStr[bInd-1]
        word += bChar
        # -> 50%: try to concatenate even the following character
        if len(word) < pwdLen and bInd < len(aStr) and randint(0,1) == 1:
            bChar = aStr[bInd]
            word += bChar

    return word

if __name__ == "__main__":
	main()
