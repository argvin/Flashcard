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
                    printCardMenu()
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
