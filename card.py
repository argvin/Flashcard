class card:
    def __init__(self,f='',b='',s='l'):
        self.front = f
        self.back = b
        self.status = s #l-learning, r-reviewing, m-mastered
        # has membership info? what deck 
        # hash for random access?
    def show(self):
        print(self.front)
    # will need a different flip for images, or type checking
    def flip(self):
        dash = '-'
        lid = ''
        for i in range(len(self.front)+4):
            lid += dash
        print(lid)
        print('| ', self.front, ' |')
        print(self.back)

    def toStr(self):
        s = ''
        s += self.front + '\n'
        s += self.back + '\n'
        s += self.status + '\n'
        return s

