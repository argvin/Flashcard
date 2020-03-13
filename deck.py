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
