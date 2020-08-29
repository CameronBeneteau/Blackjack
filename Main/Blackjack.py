#!/usr/bin/env python
# coding: utf-8

# In[5]:

import random
from pygame import * #import pygam module
from time import time as tm #import real time module

mixer.init() #initiate mixer (sound system)
font.init() #initiate font

width, height = 1200, 800 #width and height of the screen
screen = display.set_mode((1200,800)) #setting the screen
clock = time.Clock() #clock for frame rate

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True


# In[6]:


class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit


# In[7]:


class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # build Card objects and add them to the list
                self.deck.append(Card(suit,rank))
                self.deck.append(Card(suit,rank))  # TOTAL OF 3 DECKS
      
    
    def __str__(self):
        deckComp = ''  # start with an empty string
        for card in self.deck:
            deckComp += '\n '+card.__str__() # standard format for printing in the string form
        return 'The deck has:' + deckComp

    def shuffle(self):
        random.shuffle(self.deck)
        random.shuffle(self.deck)
        
    def deal(self):
        singleCard = self.deck.pop(0)
        return singleCard

# a = Deck()
# print(a)


# In[8]:


class Hand:
    
    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0   # start with zero value
        self.aces = 0    # variable to keep track of aces
    
    def addCard(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == 'Ace': #to keep track of the aces
            self.aces +=1
    
    def adjustForAce(self):
        while self.value > 21 and self.aces:
            self.value -=10
            self.aces -=1


# In[9]:


class Chips:
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
        
    def winBet(self):
        self.total+= self.bet*2
    
    def adjustTotal(self):  # Updates the total number of chips after player places bets
        self.total-= self.bet
    
    def loseBet(self):  # the total chips are always updated, so this function is not useful
        pass
    
    def push(self):
        self.total+= self.bet


# In[10]:


def takeBet(chips): #this 'chips' variable is an object of the Chips() class
    
    while True:
        
        try:
            chips.bet = int(input('How much would you like to bet?: '))
        except:
            print('Please enter a valid integer')
        else:
            if chips.bet > chips.total:
                print('Sorry, your bet needs to be less than {}'.format(chips.total))
            else:
                break


# In[11]:


def hit(deck,hand): #objects of class Deck() and Hand()
    
    someCard = deck.deal()
    hand.addCard(someCard)
    hand.adjustForAce() #adjusting for the value of the ace
    

def doubleOrNothing(chips): #doubles the bet of the player, returns True if possible, and statement if not
    
    action = input('\n Would you like to Double or Nothing? y or n: ')
    if action=='y':
        if chips.total < chips.bet: # Checks whether it is possible to double or nothing
            print("\n You don't have enough chips to double your bet.")
            return False
        else:
            chips.adjustTotal()  # Subtracts the bet from the total amount
            chips.bet = chips.bet*2
            print("\n Your bet has been doubled.")
# print(chips.bet)
# print(chips.total)
            return True
    else:
        return False


# In[12]:


def split(deck,player,dealer,chips):  # player and dealer are objects of class Hand()
# This function will create 2 seperate turns for the player to play
    
    global playing
    
    action = input('\n Would you like to split? y or n: ')
    
    if action=='y':
        if chips.total < chips.bet:  # Checks whether splitting is possible
            print("\n You don't have enough chips to split.")
        else:
                                      # ************ FIRST TURN ************ 
            print("\n Your first turn:")
            playerSplit1 = Hand()
            playerSplit1.cards.append(player.cards[0])  # Adds the player's first card to the player's new turn
            playerSplit1.addCard(deck.deal())
            showSomeCards(dealer,playerSplit1)
            
            while playing:
                hitOrStand(deck,playerSplit1)
                showSomeCards(dealer,playerSplit1)
                if playerSplit1.value > 21: # to check if player has exceeded 21
                    playerBusts(playerSplit1,dealer,chips)
                    break
            
            if playerSplit1.value <= 21:
                while dealer.value <= 17 or dealer.value < playerSplit1.value: # dealer keeps hitting till the value is at most 17 
                    hit(deck,dealer)
                
                showAllCards(dealer,playerSplit1)
            
                checking(playerSplit1,dealer,chips)  # different winning scenarios
    
                                      # ************ SECOND TURN ************ 
            print("\n Your second turn:")
            playerSplit2 = Hand()
            playerSplit2.cards.append(player.cards[1])  # Adds the player's second card to the player's new turn
            playerSplit2.addCard(deck.deal())
            showSomeCards(dealer,playerSplit2)
            
            while playing:
                hitOrStand(deck,playerSplit2)
                showSomeCards(dealer,playerSplit2)
                if playerSplit2.value > 21: # to check if player has exceeded 21
                    playerBusts(playerSplit2,dealer,chips)
                    break
            
        if playerSplit2.value <= 21:
            while dealer.value <= 17 or dealer.value < playerSplit2.value: # dealer keeps hitting till the value is at most 17 
                hit(deck,dealer)
                
            showAllCards(dealer,playerSplit2)
            
            checking(playerSplit2,dealer,chips)  # different winning scenarios


# In[13]:


def hitOrStand(deck,hand):
    
    global playing
    
    while True:
        
        action = input('\n Would you like to hit or stand? Please enter h or s: ')
        
        if action == 'h':
            hit(deck,hand)
        elif action == 's':
            print("\n Player has chosen to stand. It is now the dealer's turn.")
            playing = False
        else:
            continue
        break


# In[14]:


def showSomeCards(dealer,player): #dealer and player are both objects of the Hand() class
    
    print("\n Dealer's cards are: \n")
    print("<card hidden>")
    print(dealer.cards[1])
    print("Dealer's hand is: ____")
    print('\n')
    print("Player's cards are: \n")
    for card in player.cards:
        print(card)
    print("Player's hand is: {}".format(player.value))
        
def showAllCards(dealer,player):  #dealer and player are both objects of the Hand() class
    
    print("\n Dealer's cards are: \n")
    for a in dealer.cards:
        print(a)
    print("Dealer's hand is: {}".format(dealer.value))
    print('\n')
    print("Player's cards are: \n")
    for b in player.cards:
        print(b)
    print("Player's hand is: {}".format(player.value))


# In[15]:


def playerBusts(player,dealer,chips):  #this 'chips' variable is an object of the Chips() class
    print('\n Player busts. Better luck next time.')
    chips.loseBet()

def playerWins(player,dealer,chips):
    print('\n Player wins. Congratulations!')
    chips.winBet()

def dealerBusts(player,dealer,chips):
    print('\n Dealer busts. Congratulations!')
    chips.winBet()
    
def dealerWins(player,dealer,chips):
    print('\n Dealer wins. Better luck next time.')
    chips.loseBet()
    
def push(player,dealer,chips):
    print('\n Dear and Player have tied. It is a push!')
    chips.push()


# In[16]:


def checking(player,dealer,chips):  # checks for different end possibilities
    
    if dealer.value > 21:
        dealerBusts(player,dealer,chips)
        
    elif dealer.value > player.value:
        playerBusts(player,dealer,chips)
            
    elif dealer.value < player.value:
        playerWins(player,dealer,chips)
        
    else:
        push(player,dealer,chips)

###############################################################################
        
def loadCardImages(suit):
    cards = []
    for i in range(1,14):
        cards.append(image.load("CardImages/%d%s.png" % (i, suit)))
        screen.blit(backgroundImage, (0,0))
        screen.blit(cards[-1], (0, 0))
        display.flip()
        time.wait(100)
    return cards

###############################################################################
#OTHER_IMAGES
backgroundImage = image.load("Images/mainBackground.jpg").convert_alpha()
###############################################################################
# In[ ]:


print('\n \t \t \t \t \t \t WELCOME TO BLACKJACK! \nYou need the total value of 21 to win, and aces can be counted as either 11 or 1. You start off with **100** chips.')

playerChips = Chips()

running = True

while running:
    for e in event.get():
        display.set_caption("BLACKJACK // FPS = {0:.0f}".format(clock.get_fps()))#create caption for game
        if e.type == QUIT: #if quit
            running = False #set running to false
            
    playing = True

    heartCards = loadCardImages("H")
    diamondCards = loadCardImages("D")
    clubCards = loadCardImages("C")
    spadeCards = loadCardImages("S")
    
    deck = Deck()
    deck.shuffle()
    
    #declare the player hand 
    playerHand = Hand()        
    playerHand.addCard(deck.deal())
    playerHand.addCard(deck.deal())
    
    #declare the dealer hand
    dealerHand = Hand()        
    dealerHand.addCard(deck.deal())
    dealerHand.addCard(deck.deal())
    
    takeBet(playerChips)
    playerChips.adjustTotal()  # To remove the bet from the total number of chips
#    print(playerChips.total)
#    print(playerChips.bet)
    
    showSomeCards(dealerHand,playerHand)
    
    
   
                             # ***************START IGNORING THIS PART*****************
    
#    if playerHand.cards[0].split()[0]==playerHand.cards[1].split()[0]: # This checks if there is a condition for split
#        split(deck,playerHand,dealerHand,playerChips)
    # playerHand.cards[0] will be the first card object, and using split()[0] we can extract the first word from it.
    
                            # ***************STOP IGNORING THIS PART*****************
       
        
    DoN = doubleOrNothing(playerChips)  # Has a value of True/False depending on action of player
    
    while playing:
        
        if DoN: # if DoN is True, the player hits ONLY once more, then it is the dealer's turn
            hit(deck,playerHand)
            showSomeCards(dealerHand,playerHand)
            break
        
        else:
            hitOrStand(deck,playerHand)
            showSomeCards(dealerHand,playerHand)
            
            if playerHand.value > 21: # to check if player has exceeded 21
                playerBusts(playerHand,dealerHand,playerChips)
                break
    
    if playerHand.value <= 21:
        
        while dealerHand.value <= 17 or dealerHand.value < playerHand.value: # dealer keeps hitting till the value is at most 17 
            hit(deck,dealerHand)
        
        showAllCards(dealerHand,playerHand)
        
        checking(playerHand,dealerHand,playerChips)  # different winning scenarios
    
    print('\n You now have a total of {}'.format(playerChips.total) + ' chips')
    
    ask = input('\n Would you like to play again? y or n: ')
    
    if ask == 'y':
        continue
    else:
        break
    
    display.flip() #blit everything on the screen
    clock.tick(60) #frame rate is 60
    
display.flip() #blit everything on the screen

print('\n Thank you for playing Blackjack.')


# In[ ]:





# In[ ]:




