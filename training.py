import urllib.request
import json

#Using global variables so I do not need to pass variables around
textNumbers = [84,            1342,                  25344,                46,                 11,                                  345,       2701,       2542,             1661,                               76,                 98]
textTitles = ["Frankenstein", "Pride and Prejudice", "The Scarlet Letter", "A Christmas Carol", "Alice’s Adventures in Wonderland", "Dracula", "Moby-Dick", "A Doll’s House", "The Adventures of Sherlock Holmes", "HUCKLEBERRY FINN", "A TALE OF TWO CITIES"]

maxLetterCount = 5
letterCount = {}
validCharacters = list("abcdefghijklmnopqrstuvwxyz .!?,")


#main function will initiate getting the data and writing to file
#also outputs the state as we are running
def main():
    print("Getting Data")
    getData()
    
    print("Writing to File")
    writeToFile()

    print("Complete")


#getData function calls website URL and gets the text back
# it also looks through each character it gets back and adds it to the queue
def getData():
    global textNumbers
    global textTitles

    char_queue = []

    #we loop through the titles and their id's
    for i, title in zip(textNumbers, textTitles):

        #we print the title and then we call the gutenberg website to get the text data
        print(title)
        try:
            with urllib.request.urlopen(f'https://www.gutenberg.org/files/{i}/{i}-0.txt') as f:

                # we then loop through each character and add it to the queue
                for ch in f.read().decode('utf-8'):

                    #gutenberg likes to combine characters together and give us inaccurate data
                    if(ch == "æ"):
                        char_queue = addToQueue("a", char_queue)
                        char_queue = addToQueue("e", char_queue)
                    elif(ch == "œ"):
                        char_queue = addToQueue("o", char_queue)
                        char_queue = addToQueue("e", char_queue)
                    elif(ch == "ꝏ"):
                        char_queue = addToQueue("o", char_queue)
                        char_queue = addToQueue("o", char_queue)
                    else:
                        char_queue = addToQueue(ch, char_queue)

        #if we get an error we will print it
        except urllib.error.URLError as e:
            print(e.reason)

#addToQueue function adds a character to the queue if it is valid
#queue is bounded by the maxCharacterCount
#it will then loop through the queue and add each section of the queue into the letterCount dict
#returns the append-ed queue
def addToQueue(char, char_queue):
    global validCharacters
    global maxLetterCount
    global letterCount

    #converts the character to lowercase and validates that it is in the valid characters
    #if not we will reset the queue so we do not get weird data
    lowerChar = char.lower()
    if(not lowerChar in validCharacters):
        return []

    #we then append the letter and if the queue is too long we will pop the first item off the queue
    char_queue.append(lowerChar)
    if(len(char_queue) > maxLetterCount):
        char_queue.pop(0)

    #we will then loop from the front to the back of the queue and get each section
    #those sections will tell us which characters come before the last character in queue
    #we will then increment that substring in the dict
    for index,_ in enumerate(char_queue):
        joinedString = ""
        joinedString = joinedString.join(char_queue[index:])
        if(joinedString in letterCount):
            letterCount[joinedString] += 1
        else:
            letterCount[joinedString] = 1


    return char_queue


#writeToFile function dumps the json data into a text file for later use
def writeToFile():
    global letterCount

    with open('letter_count.txt', 'w') as file:
        file.write(json.dumps(letterCount))


#checks to make sure we are running the file directly
if __name__ == '__main__':
    main()