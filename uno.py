### Thanks https://www.youtube.com/@lasplagasm

import random
import pandas as pd #is this slower than python native?
from time import sleep

# Watch these lazy skills
deckValueInput = "0123456789123456789rrss++" # Fills coloured part of deck
deckWildInput = "wwwwffff"
# CARD TYPE MEANINGS
# number = value
# r = Reverse
# s = Skip
# + = +2 draw
# w = Wild
# f = +4 draw (f in chat)
deckColourInput = ["blue", "red", "green", "yellow"] # Used in some logic too

class Card:
	type = "if these values comes up in a game"
	colour = "thats bad"
	def __init__(self, type, colour): # why are python constructors like that
		self.type = type
		self.colour = colour

	def __repr__(self) -> str:
		return f'{self.type}, {self.colour}'
    
class Deck:
	cards = []
	def reset(self):
		for colour in deckColourInput:
			for value in deckValueInput:
				self.cards.append(Card(value,colour))
		for wild in deckWildInput:
			self.cards.append(Card(wild,'wild'))

	def __repr__(self):
		deck_df = pd.DataFrame({
			'type': [card.type for card in self.cards],
			'colour' : [card.colour for card in self.cards]
		})
		return f'Deck: {deck_df}'
	

	def draw(self, discard): # Draw a random card
		if(len(self.cards) < 1): # Deck almost empty, draw and add unused cards in discard pile
			self.cards = discard.copy()
			discard.clear()
		index = random.randint(0, len(self.cards)-1)
		card = self.cards[index]
		del self.cards[index]

		return card

class Player: # Default player is user controlled
	name = "default"
	wins = 0
	def __init__(self, playername):
		self.name = playername
	def turn(self, hand, lastDiscard): # Choosing discard
		while True:
			print(f"discard: {lastDiscard.type} {lastDiscard.colour}")
			for i in range(len(hand)):
				print(f'{i} = {hand[i]}')
			discardAttempt = int(input("Which card?"))
			if(discardAttempt == len(hand)):
				return "draw"
			if(turncheck(hand[discardAttempt], lastDiscard)):
				return discardAttempt
	def colourselect(self, hand, lastDiscard): # Choosing colour after using wild
		for i in range(4):
			print(f'{i} = deckColourInput[i]')
		return deckColourInput[int(input("Which colour?"))]

def turncheck(discardAttempt, lastDiscard): # Checks if a move is valid
	if(discardAttempt.colour == "wild"):
		return True
	if(discardAttempt.colour == lastDiscard.colour):
		return True
	if(discardAttempt.type == lastDiscard.type):
		return True
	return False

def startGame(players, deck, discard, slow = False): # Start game with players array as parameter
	deck.reset()
	discard.clear()
	hands = []
	for i in range(len(players)): # FILL PLAYER HANDS
		hands.insert(len(hands), [])
		for j in range(7):
			hands[i].insert(len(hands[i]), deck.draw(discard))

	lastDiscard = deck.draw(discard)

	skip = False
	draw2 = False
	draw4 = False

	# Shuffle order of players
	for i in range(random.randint(0, len(players)-1)):
		players = [players[-1]] + players[:-1]

	# GAME LOOP
	while True:
		for i in range(len(players)): # Turns
			print("PLAYER: "+ players[i].name)

			# CHECKING CARD EFFECTS
			if(skip):
				skip = False
				continue # Skip turn
			elif(draw2):
				for j  in range(2):
					hands[i].insert(len(hands[i]), deck.draw(discard)) # Draw 2
				draw2 = False
				continue # Skip turn
			elif(draw4):
				for j  in range(4):
					hands[i].insert(len(hands[i]), deck.draw(discard)) # Draw 4
				draw4 = False
				continue # Skip turn
			
			if(players[i].name == "MegaBot"):
				discardIndex = players[i].turn(hands[i], lastDiscard, hands)
			else:
				discardIndex = players[i].turn(hands[i], lastDiscard) # Gets player's choice
			if(discardIndex == "draw"): # Draw and forfeit turn
				hands[i].insert(len(hands[i]), deck.draw(discard))
				print(players[i].name + " draws!" + " Card count: " + str(len(hands[i])))
				continue # this holds up the whole world together

			discard.insert(len(discard), lastDiscard)
			lastDiscard = hands[i][discardIndex] # Updating the last discard
			del hands[i][discardIndex] # Remove discard from hand
			print(players[i].name + " discards: " + lastDiscard.type + " " + lastDiscard.colour + ". Card count: " + str(len(hands[i])))

			# CHECKING FOR VICTORY
			if(len(hands[i]) == 0):
				print("the winner is: "+players[i].name)
				players[i].wins += 1
				return
			
			# CHECKING CARD NEW EFFECT
			if(lastDiscard.colour == "wild"): # Wild: colour select
				lastDiscard.colour = players[i].colourselect(hands[i], lastDiscard) # Update colour
				if(lastDiscard.type == "f"): # +4
					draw4 = True
			elif(lastDiscard.type == "r"): # Reverse
				# Reverse around pivot i
				revplayers = players.copy() # i wasted 30 minutes not knowing i needed to use .copy() lol
				revplayers.reverse()
				while(revplayers[i].name != players[i].name):
					revplayers = [revplayers[-1]] + revplayers[:-1]
				players = revplayers
			elif(lastDiscard.type == "s"): # Skip
				skip = True
			elif(lastDiscard.type == "+"): # Draw 2
				draw2 = True
			if slow:
				sleep(2)

if __name__ == '__main__':
	# Defining global deck and discard pile bc its easier that way :D
	deck = Deck()
	discard = []
	players = [Player(f'Player {i}') for i in range(2)]
	startGame(players, deck, discard)
