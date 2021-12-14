import json

letterCount = {}

def main():
    readFromFile()
    print(letterCount["i"])


def readFromFile():
    global letterCount
    with open('letter_count.txt') as file:
        letterCount = json.load(file)


#checks to make sure we are running the file directly
if (__name__ == "__main__"):
    main()