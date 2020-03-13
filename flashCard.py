import os
import random as rand
from card import *
from deck import *
from deckHandler import *

# TODO make cards with math formulas / latex
# TODO make cards use images, os.command('imshow X')
#		when creating card, just give it image filepath
# TODO pretty print the card in a box with status displayed

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

def printCardMenu():
    print('--------------------')
    print('m - master')
    print('n - next')
    print('--------------------')


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

		

