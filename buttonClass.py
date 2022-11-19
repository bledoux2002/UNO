# buttonClass.py, created by Benjamin Ledoux
# The purpose of this program is to provide a universal button class 

from graphics import *

class Button:

    """A button is a labeled rectangle in a window.
    It is enabled or disabled with the activate()
    and deactivate() methods. The clicked(pt) method
    returns True if and only if the button is enabled and pt is inside it."""


    def __init__(self, win, center, width, height, label):

        """ Creates a rectangular button, eg:
        quitButton = Button(myWin, centerPoint, width, height, 'Quit') """ 
        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()

        # Hold the extremes of the button shape (top, bottom, left, right)
        self.xmax, self.xmin = x+w, x-w 
        self.ymax, self.ymin = y+h, y-h

        # Top left and bottom right extremes used for Rectangle()
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)

        # Place label at center of button
        self.label = Text(center, label)
        self.label.draw(win)
        self.active = True #this variable keeps track of whether or not the button is currently "active"


    def getLabel(self):

        "Returns the label string of this button."
        return self.label.getText()


    def activate(self):

        "Sets this button to 'active'."
        self.label.setFill('black') #color the text "black"
        self.rect.setWidth(1)       #set the outline to look bolder
        self.active = True          #set the boolean variable that tracks "active"-ness to True


    def deactivate(self):

        "Sets this button to 'inactive'."
        self.label.setFill('darkgray')
        self.rect.setWidth(1)
        self.active = False          


    def draw(self, win):

        "Draws button to win and activates it."
        self.rect.draw(win)
        self.label.draw(win)
        self.activate()

    def undraw(self):

        "Undraws button from win and deactivates it."
        self.deactivate()
        self.rect.undraw()
        self.label.undraw()


    def clicked(self, p):

        "Returns true if button active and Point p is inside"
        return (self.active and

                self.xmin < p.getX() < self.xmax and

                self.ymin < p.getY() < self.ymax)
    
