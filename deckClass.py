# deckClass.py, created by Benjamin Ledoux
# This creates a class for a deck of playing cards

from playingCardClass import *
from random import *

class Deck:
    def __init__(self):
        self.cardList = []
        for c in ["b", "g", "r", "y"]:
            for r in range(11): # Changed from 13 to 10 to omit utility cards
                self.cardList.append(PlayingCard(r, c))

    def shuffleDeck(self):
        shuffle(self.cardList)

    def dealCard(self):
        self.card = self.cardList[0]
        self.cardList.remove(self.cardList[0])
        return self.card
    
    def cardsLeft(self):
        return len(self.cardList)
