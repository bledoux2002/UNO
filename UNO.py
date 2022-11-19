# UNO.py, by Benjamin Ledoux
# The purpose of this program is to simulate a game of 'UNO!' between a player and a computer.

# Import modules
from graphics import *
from deckClass import *
from buttonClass import *
from random import *
import time
"""
graphics is used to display the game
deckclass makes a deck of cards from the playingcardclass module
buttonClass makes fully functional buttons for the UI
random lets the pile of cards played look more natural and accurate to a real life game of UNO!
time is used to space out different UI and game board changes for easier processing by the PC
"""

# Creates a class that simulates a game of UNO
# This class will provide everything needed to simulate a game of UNO.
class Uno:

    # Initializes the variables and lists, creates a new deck of cards from deckclass.py, and uses its .shuffleDeck() method to shuffle it.
    # opntHand and playerHand will hold the cards of each hand from playingcardclass.py, while oHandImg and pHandImg will hold the associated images.
    # playingDeck will hold the deck of cards from deckclass.py used for this instance of the game.
    def __init__(self, opntHand, playerHand, tableDeck):

        # Lists for cards
        self.playerHand = playerHand
        self.opntHand = opntHand
        self.tableDeck = tableDeck

        # Images for cards
        self.pHandImg = []
        self.oHandImg = []

        # Coordinates of images
        self.pCoords = []
        self.oCoords = []
        self.oHandCover = []

        # Images of decks
        self.tDeckImg = [] # played cards
        self.pDeckImg = None # undrawn cards

        # Create and shuffle new deck of cards
        self.playingDeck = Deck()
        self.playingDeck.shuffleDeck()

    # This method uses the deckclass dealCard() method to deal 4 cards each to the opponent and player, adding them to the instance lists for each hand.
    # It then finds the associated image in the playingcards folder and displays them in a GraphWin, adding them to the image lists.
    # It takes inputted x and y coordinates for the location on the GraphWin where the card images will show up.
    def initDeal(self, win, xposO, yposO, xposP, yposP):

        for i in range(4):

            # Add new card to each hand
            self.opntHand.append(self.playingDeck.dealCard())
            self.playerHand.append(self.playingDeck.dealCard())

            # Record coordinates of each image
            self.oCoords.append(Point(xposO - (100 * i), yposO))
            self.pCoords.append(Point(xposP + (100 * i), yposP))

            # Add corresponding image to game board
            self.oHandImg.append(Image(self.oCoords[i], "cardassets/" + self.opntHand[i].__str__() + ".png"))
            self.oHandCover.append(Image(self.oCoords[i], "cardassets/cardBack.png"))
            self.pHandImg.append(Image(self.pCoords[i], "cardassets/" + self.playerHand[i].__str__() + ".png"))

            # Space out dealing of cards
            time.sleep(0.125)
            self.oHandCover[i].draw(win)
            time.sleep(0.25)
            self.pHandImg[i].draw(win)
            time.sleep(0.125)

        # Print current contents of each hand for debugging purposes
        """
        for card in self.opntHand:
            print(card.__str__(), end = " ")
        print()
        for card in self.playerHand:
            print(card.__str__(), end = " ")
        """

        # Take top card of playingDeck and play to tableDeck
        self.tableDeck.append(self.playingDeck.dealCard())
        self.tDeckImg.append(Image(Point(500, 500), "cardassets/" + self.tableDeck[0].__str__() + ".png"))
        self.tDeckImg[0].draw(win)

        # Show playingDeck on side of game board
        self.pDeckImg = Image(Point(750, 500), "cardassets/cardBack.png")
        self.pDeckImg.draw(win)

    # Plays a card from hand to tableDeck.
    def playCard(self, win, hand, imgList, coList, pos):

        self.pos = pos # Takes position of card in hand.
        self.comp = True

        # Go thru cards in opntHand, if not compatible with center card, check next card, otherwise continue with current card
        if hand == self.opntHand:
            for c in range(len(hand)):
                if self.compatible(hand[c]) != True:
                    self.pos = self.pos + 1
                elif self.compatible(hand[c]) == True:
                    break

        # If no compatible cards found, set hand compatibility to false and end method
        if self.pos == len(hand):
            self.comp = False
            return

        # Moves current card from hand to tableDeck
        self.tableDeck.append(hand.pop(self.pos)

        # Moves corresponding image from imgList to tDeckImg.
        self.tDeckImg.append(Image(Point(500 + randrange(-25, 25), 500 + randrange(-25, 25)), "cardassets/" + self.tableDeck[-1].__str__() + ".png"))
        self.tDeckImg[-1].draw(win)

        # Removes current card image from hand
        imgList[self.pos].undraw()
        del imgList[self.pos]
        if imgList == self.oHandImg:
            self.oHandCover[self.pos].undraw()
            del self.oHandCover[self.pos]

        del coList[self.pos]

        # Shifts rest of cards over according to where they are on the board.
        for i in range(len(imgList[self.pos:])):
            if hand == self.playerHand:
                imgList[self.pos + i].move(-100, 0)
                coList[self.pos + i] = Point(coList[self.pos + i].getX() - 100, coList[self.pos + i].getY())
            else:
                imgList[self.pos + i].move(100, 0)
                self.oHandCover[self.pos + i].move(100, 0)
                coList[self.pos + i] = Point(coList[self.pos + i].getX() + 100, coList[self.pos + i].getY()) 

        # Print current contents of hand for debugging purposes
        """
        for card in hand:
            print(card.__str__(), end = " ")
        print()
        """

    # Return boolean of card caompatibility with center card
    def compatible(self, card):

        if card.getRank() == self.tableDeck[-1].getRank() or card.getColor() == self.tableDeck[-1].getColor():
            return True

    # Takes top card from playingDeck and places in hand
    def drawCard(self, win, hand, imgList, coList):

        # Go thru tableDeck and remove all but top card and place them back into playingDeck
        if len(self.playingDeck.cardList) == 0:
            for c in range(len(self.tableDeck) - 1):
                self.playingDeck.cardList.append(self.tableDeck.pop(0))
                self.tDeckImg.pop(0).undraw()
            self.playingDeck.shuffleDeck()
            self.pDeckImg.draw(win)

        # Adds card from top of playingDeck to hand.
        hand.append(self.playingDeck.dealCard())

        # Adds corresponding image(s) to proper hand and draws them to window.
        if hand == self.playerHand:
            coList.append(Point(coList[-1].getX() + (100), coList[-1].getY()))
            imgList.append(Image(coList[-1], "cardassets/" + hand[-1].__str__() + ".png"))
            imgList[-1].draw(win)
        else:
            coList.append(Point(coList[-1].getX() - (100), coList[-1].getY()))
            imgList.append(Image(coList[-1], "cardassets/" + hand[-1].__str__() + ".png"))
            self.oHandCover.append(Image(coList[-1], "cardassets/cardBack.png"))
            self.oHandCover[-1].draw(win)

        # If no cards left in playingDeck, undraw representative image
        if len(self.playingDeck.cardList) == 0:
            self.pDeckImg.undraw()


def main():

    # Create GraphWin for game
    gWin = GraphWin("UNO!", 1000, 1000)
    gWin.setBackground('lightblue')

    # Set up Splash Screen
    welcomeLbl = Text(Point(500, 250), "Welcome to UNO!")
    welcomeLbl.setSize(36)
    welcomeLbl.draw(gWin)

    # Initialize all buttons
    # Main Menu
    startBtn = Button(gWin, Point(500, 800), 200, 75, "BEGIN!")
    quitBtn = Button(gWin, Point(950, 950), 75, 25, "QUIT")
    rulesBtn = Button(gWin, Point(950, 925), 75, 25, "RULES")

    # Game Menu
    resetBtn = Button(gWin, Point(950, 900), 75, 25, "RESTART")
    drawBtn = Button(gWin, Point(750, 625), 75, 25, "DRAW")
    pHandBtn = []
    for n in range(8):
        pHandBtn.append(Button(gWin, Point(100 + (100 * n), 750), 75, 25, str(n + 1)))
        pHandBtn[n].undraw()

    # Adjusts UI to only show 
    drawBtn.undraw()
    resetBtn.undraw()

    pt = gWin.getMouse()

    # While quit button hasn't been clicked, check for other buttons if they've been clicked
    while quitBtn.clicked(pt) == False:

        # if "Rules" button is clicked, opens new window with uno_rules.txt
        if rulesBtn.clicked(pt) == True:

            rWin = GraphWin("UNO! Rules", 750, 500)
            rWin.setBackground('lightblue')
            rulesTxt = open('uno_rules.txt', 'r', encoding = 'UTF-8')
            rulesLbl = Text(Point(375, 250), rulesTxt.read())
            rulesLbl.draw(rWin)


        # If "BEGIN!" button is clicked, sets up a new game of UNO!
        elif startBtn.clicked(pt) == True:

            welcomeLbl.undraw()
            startBtn.undraw()

            # Creates lists for use in UNO! game, initializes UNO! class under 'game'
            oHand = []
            pHand = []
            tDeck = []
                
            game = Uno(oHand, pHand, tDeck)
                
            # Sets up buttons, hands out initial cards with initDeal() method
            game.initDeal(gWin, 850, 100, 100, 875)
            for i in range(4):
                pHandBtn[i].draw(gWin)
                if game.compatible(game.playerHand[i]) != True:
                    pHandBtn[i].deactivate()
            resetBtn.draw(gWin)
            drawBtn.draw(gWin)


        # Takes the card button pressed and plays the corresponding card, then moves on to opponent's turn.
        for b in range(len(pHandBtn)):

            if pHandBtn[b].clicked(pt) == True:

                # Player turn
                game.playCard(gWin, game.playerHand, game.pHandImg, game.pCoords, b)
                pHandBtn[len(game.playerHand)].undraw()
                for c in range(len(game.playerHand)):
                    pHandBtn[c].deactivate()
                drawBtn.deactivate()

                if len(game.playerHand) < 8:
                    drawBtn.label.setText("DRAW")

                # If a +2 card is played, attempt to add two cards to recipient's hand.
                if game.tableDeck[-1].getRank() == 10:
                    for i in range(2):
                        if len(game.opntHand) < 8:
                            game.drawCard(gWin, game.opntHand, game.oHandImg, game.oCoords)

                # Determines if player hand is empty.
                if len(game.playerHand) == 0:
                    welcomeLbl.setText("YOU WIN!")
                    welcomeLbl.draw(gWin)
                    break

                # Pause using time here so opponent takes a moment before playing.
                time.sleep(1)

                # Opponent turn
                game.playCard(gWin, game.opntHand, game.oHandImg, game.oCoords, 0)
                if game.comp != False and game.tableDeck[-1].getRank() == 10: # If a +2 card is played, attempt to add two cards to recipient's hand.
                    for i in range(2):
                        if len(game.playerHand) < 8:
                            game.drawCard(gWin, game.playerHand, game.pHandImg, game.pCoords)
                            pHandBtn[len(game.playerHand) - 1].draw(gWin)
                            pHandBtn[len(game.playerHand) - 1].deactivate()
                    if len(game.playerHand) == 8:
                        drawBtn.label.setText("PASS")
                elif game.comp == False and len(game.opntHand) < 8: # If the opponent didn't play card and has room, they draw a card.
                    game.drawCard(gWin, game.opntHand, game.oHandImg, game.oCoords)
                elif len(game.opntHand) == 0: # Determines if opponent hand is empty.
                    welcomeLbl.setText("YOU LOSE!")
                    welcomeLbl.draw(gWin)
                    break

                # Sets player hand buttons according to if they're compatible with the center card or not.
                for e in range(len(game.playerHand)):
                    if game.compatible(game.playerHand[e]) != True:
                        pHandBtn[e].deactivate()
                    elif game.compatible(game.playerHand[e]) == True:
                        pHandBtn[e].activate()
                drawBtn.activate()


        # Draws card to playerHand, then proceeds to opponent's turn.
        if drawBtn.clicked(pt) == True:

            # Player turn
            if len(game.playerHand) < 8:
                game.drawCard(gWin, game.playerHand, game.pHandImg, game.pCoords)
                pHandBtn[len(game.playerHand) - 1].draw(gWin)
            for c in range(len(game.playerHand)):
                pHandBtn[c].deactivate()
            drawBtn.deactivate()
            if len(game.playerHand) == 8:
                drawBtn.label.setText("PASS")

            # Pause using time here so opponent hand takes a moment before playing
            time.sleep(1)

            # Opponent turn
            game.playCard(gWin, game.opntHand, game.oHandImg, game.oCoords, 0)
            if game.comp != False and game.tableDeck[-1].getRank() == 10: # If a +2 card is played, attempt to add two cards to recipient's hand.
                for i in range(2):
                    if len(game.playerHand) < 8:
                        game.drawCard(gWin, game.playerHand, game.pHandImg, game.pCoords)
                        pHandBtn[len(game.playerHand) - 1].draw(gWin)
                        pHandBtn[len(game.playerHand) - 1].deactivate()
                if len(game.playerHand) == 8:
                    drawBtn.label.setText("PASS")
            elif game.comp == False and len(game.opntHand) < 8: # If the opponent didn't play card and has room, they draw a card.
                game.drawCard(gWin, game.opntHand, game.oHandImg, game.oCoords)
            elif len(game.opntHand) == 0: # Determines if opponent hand is empty.
                welcomeLbl.setText("YOU LOSE!") #add sad sound
                welcomeLbl.draw(gWin)
                continue


            # Sets player hand buttons according to if they're compatible with the center card or not.
            for d in range(len(game.playerHand)):
                if game.compatible(game.playerHand[d]) != True:
                    pHandBtn[d].deactivate()
                elif game.compatible(game.playerHand[d]) == True:
                    pHandBtn[d].activate()
            drawBtn.activate()

            # Determine if game is tied and no winner can be determined (no room for more cards in either hand, no compatible cards in either hand)
            if len(game.playerHand) == 8 and len(game.opntHand) == 8:
                tie = True
                for card in game.playerHand:
                    if game.compatible(card) == True:
                        tie = False
                for  card in game.opntHand:
                    if game.compatible(card) == True:
                        tie = False
                if tie == True: # If neither hand has a playable card, the game counts as a draw to prevent an infinite loop of passing turns.
                    welcomeLbl.setText("It's a draw!")
                    welcomeLbl.draw(gWin)
                    continue


        elif resetBtn.clicked(pt) == True: # Resets UI to main menu as if window was just opened.

            # Undraws UI from previous game
            for image in game.oHandCover:
                image.undraw()
            for image in game.pHandImg:
                image.undraw()
            for image in game.tDeckImg:
                image.undraw()
            game.pDeckImg.undraw()

            for btn in pHandBtn:
                btn.undraw()

            welcomeLbl.setText("Welcome to UNO!")
            startBtn.draw(gWin)
            drawBtn.label.setText("DRAW")
            drawBtn.undraw()

            resetBtn.undraw()


        pt = gWin.getMouse()


    gWin.close()


main()
