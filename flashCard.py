import os
import random as rand

# TODO make cards with math formulas / latex
# TODO make cards use images, os.command('imshow X')
#		when creating card, just give it image filepath

# TODO pretty print the card in a box with status displayed

class card:
    def __init__(self,f='',b='',s='l'):
        self.front = f
        self.back = b
        self.status = s #l-learning, r-reviewing, m-mastered
        # has membership info? what deck 
        # hash for random access?
    def show(self):
        print(self.front)
    def flip(self):
        print(self.back)
    def toStr(self):
        s = ''
        s += self.front + '\n'
        s += self.back + '\n'
        s += self.status + '\n'
        return s

class deck:
    def __init__(self):
        self.cards = []
        self.title = ''
        self.status = '' # learning , reviewing , mastered (l r m)
    def shuffle(self):
        rand.shuffle(self.cards)
    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop() # TODO select and pop random element
    def add(self,card):
        self.cards.append(card) 
    def empty(self):
        return len(self.cards) == 0


###############§ Utility
def copyFile(fname):
    global deckPath
    copy = open(deckPath + fname + '_copy','w')
    inf = open(fname,'r')
    if copy.write(inf.read()) > 0:
        return True
    return False

def printMainMenu():
    print('-------------------------------------------------------------------')
    print('load or create new deck:  l <deck name>') 
    print('quit: q')
    print('-------------------------------------------------------------------')

def printDeckMenu(deckName):
    print('-------------------------------------------------------------------')
    print('Deck:  ',deckName.upper()) # maybe make a fun ascii title print
    print('add card: a <front> <CR> <back>')
    print('next card: n, (type n again to flip)')
    print('master card : m')
    print('quit to main menu: q')
    #print('\t note: promotes card status until card mastered') # should appear in help menu
    print('-------------------------------------------------------------------')

###############§ Application
class deckHandler:
    #def __init__(self,learningDeck=deck(), dfp):
    def __init__(self,_deckNames):
        self.learning = deck()
        self.reviewing = deck()
        self.mastered = deck()
        self.deckName = ''
        self.deckNames = _deckNames
        self.deckfp = None

    def openDeck(self,deckName):
        self.deckName = deckName
        #open/create file
        # TODO make copy of file justin case 
        # TODO calculate max amount of cards you could have in program memory
        # TODO think about whether or not you should keep the file open and just write to that thing in addition 
        # to maintaining a local copy of things...
        if deckName in self.deckNames:
            self.deckfp = open(deckPath + deckName,'r+')
            #read in and close -> localDeck
            self.load()
        else:
            # TODO make copy of file justin case , write to both? hmmmm
            self.deckfp = open(deckPath + deckName,'x+')
        print('openDeck::deckfp: ',self.deckfp)

    def load(self):
        line = 'bah'
        while line != '':
            cardData = card()
            line = self.deckfp.readline()
            if line != '':
                cardData.front = line
                cardData.back = self.deckfp.readline() # when making new cards, strip newlines to make all on one line
                cardData.status = self.deckfp.readline()
                # populate appropriate deck
                if cardData.status == 'l':
                    self.learning.add(cardData)
                elif cardData.status == 'r':
                    self.reviewing.add(cardData)
                else:
                    self.mastered.add(cardData)
    # write all the cards to the file 
    # learning -> reviewing -> mastered
    def write(self):
        # TODO set a flag so that you could check if it's a new addition,
        # then you don't have to rewrite things already there 
        for card in self.learning.cards:
            self.deckfp.write(card.toStr())
        for card in self.reviewing.cards:
            self.deckfp.write(card.toStr())
        for card in self.mastered.cards:
            self.deckfp.write(card.toStr())

    def quit(self):
        self.deckfp.close()

    def deckLoop(self):
        usrInput = ''
        printDeckMenu(self.deckName)
        while usrInput != 'q':
            usrInput = input('§ ')
            if len(usrInput) == 0:
                continue
            if usrInput[0] == 'n':
                cardFromDeck = self.selectCard()
                if cardFromDeck is None:
                    print('Deck is empty')
                    continue
                cardFromDeck.show()
                usrInput = input('§ ')	
                if usrInput == 'n':
                    cardFromDeck.flip()
                    print('m - master')
                    print('n - next')
                    usrInput = input('§ ')	
                    if usrInput == 'm':
                        # TODO add counts to cardFromDecks to decide whether or not to upgrade to better deck
                        if cardFromDeck.status == 'l':
                            cardFromDeck.status = 'r'
                            self.reviewing.add(cardFromDeck)
                        elif cardFromDeck.status == 'r':
                            cardFromDeck.status = 'm'
                            self.mastered.add(cardFromDeck)
                    else:
                        # recycle into learning deck
                        self.learning.add(cardFromDeck)
            elif usrInput[0] == 'a':
                front = usrInput[2:]
                print('front-§ ', front) # TODO replace with fun to handle images and text
                back = input('back-§ ')
                #back = back.strip('\n') # TODO see how to enter multiple lines ...
                self.learning.add(card(front,back))
        # finished using deck, write changes to file
        # then remove copy
        self.write()
        self.quit()

    def selectCard(self):
        # return random card for now,
        # need pq or something for picking cards out nicely
        # TODO picks from learning only rn
        return self.learning.draw()

###############§ Main
def mainLoop(deckNames):
    usrInput = ''
    dealer = deckHandler(deckNames)
    while usrInput != 'q': 
        printMainMenu()
        usrInput = input('§ ')
        if len(usrInput) == 0:
            continue
        action = usrInput[0]
        if action == 'l': # load deck or new deck
            deckName = usrInput[2:]
            deckName = deckName.lower()
            dealer.openDeck(deckName) # add these params (deckNames,deckNames) when you want to check for preexisting deck 
            dealer.deckLoop() # run() maybe should spawn a thread, that way you could error handle instead of main application crashing?
    print('Ciao')

###############§ Globals
deckPath = './Decks/' # TODO redfine path during installation

if __name__ == '__main__':
    # load deck names, compare to determine if new deck or preexisting deck
    deckNames = [d.lower() for d in os.listdir(deckPath)]
    print(deckNames)
    mainLoop(deckNames)

		

