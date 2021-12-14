import urllib.request
import json


maxLetterCount = 5
letterCount = {}
validCharacters = list("abcdefghijklmnopqrstuvwxyz .!?,")


def main():    
    textNumbers = [84,            1342,                  25344,                46,                 11,                                  345,       2701,       2542,             1661,                               76,                 98]
    textTitles = ["Frankenstein", "Pride and Prejudice", "The Scarlet Letter", "A Christmas Carol", "Alice’s Adventures in Wonderland", "Dracula", "Moby-Dick", "A Doll’s House", "The Adventures of Sherlock Holmes", "HUCKLEBERRY FINN", "A TALE OF TWO CITIES"]

    # print("Creating Map")
    # recursiveLetterString(maxLetterCount)
    
    print("Getting Data")
    getData(textNumbers, textTitles)
    
    print("Writing to File")
    writeToFile()

    print("Complete")

# def recursiveLetterString(depthCount, currentString = ""):
#     if currentString != "":
#         letterCount[currentString] = 0

#     if depthCount == 0 :
#         return

#     for i in validCharacters:
#         recursiveLetterString(depthCount - 1, currentString + i)


def getData(textNumbers, textTitles):
    char_queue = []
    for i, title in zip(textNumbers, textTitles):
        print(title)
        try:
            with urllib.request.urlopen(f'https://www.gutenberg.org/files/{i}/{i}-0.txt') as f:
                for ch in f.read().decode('utf-8'):
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


        except urllib.error.URLError as e:
            print(e.reason)


def addToQueue(char, char_queue):
    lowerChar = char.lower()
    if(not lowerChar in validCharacters):
        return []

    char_queue.append(lowerChar)
    if(len(char_queue) > maxLetterCount):
        char_queue.pop(0)

    for index,_ in enumerate(char_queue):
        joinedString = ""
        joinedString = joinedString.join(char_queue[index:])
        if(joinedString in letterCount):
            letterCount[joinedString] += 1
        else:
            letterCount[joinedString] = 1


    return char_queue

def writeToFile():
    with open('letter_count.txt', 'w') as file:
        file.write(json.dumps(letterCount))



if __name__ == '__main__':
    main()