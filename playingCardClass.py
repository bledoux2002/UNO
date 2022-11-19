# playingCardClass.py, created by Benjamin Ledoux
# This creates a class for each playing card

class PlayingCard():
    
    def __init__(self, rank, color):
        self.rank = rank
        self.color = color

    def getRank(self):
        return self.rank

    def getColor(self):
        return self.color

    def __str__(self):
        return self.color + str(self.rank)
