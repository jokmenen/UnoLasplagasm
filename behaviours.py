### Thanks https://www.youtube.com/@lasplagasm

from uno import *
from statistics import mode
from tqdm import tqdm

# Make bot classes with their own functions here
# Note: To draw, return "draw" in turn. To discard, return index of card in hand
class Randy(Player): # Randy is completely random
  name = "Randy"
  def turn(self, hand, lastDiscard): # Choosing discard
    while True:
      discardAttempt = random.randint(0, len(hand))
      if(discardAttempt == len(hand)):
        return "draw"
      if(turncheck(hand[discardAttempt], lastDiscard)):
        return discardAttempt
  def colourselect(self, hand, lastDiscard): # Choosing colour after using wild
    return deckColourInput[random.randint(0, 3)]
  
class Mandy(Player): # Mandy uses common-sense priorities, trying to get the same colours out the way first
  name = "Mandy"
  # Turn priority:
  # Match Colour with Numbered Card
  # Match Number with Numbered Card
  # Match Colour/Type with Special Coloured Card
  # Wild/+4
  # Draw
  # am i gonna do this with a buncha thoughtless loops? absolutely!
  def turn(self, hand, lastDiscard): # Choosing discard. No need to check validity of move since logic is in method
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].type == lastDiscard.type and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour or hand[i].type == lastDiscard.type):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == "wild"):
        return i
    return "draw"
  # Colour select:
  # Select the most common colour in hand
  # If hand is all wilds, select random colour
  def colourselect(self, hand, lastDiscard): # Choosing colour after using wild
    listForConvenience = []
    for i in hand:
      if(i.colour == "wild"):
        continue
      listForConvenience.insert(len(listForConvenience), i.colour)
    if(len(listForConvenience) == 0):
      return deckColourInput[random.randint(0, 3)]
    return mode(listForConvenience)
  
class Nancy(Player): # Nancy is like Mandy but she tries to switch colours as much as possible
  name = "Nancy"
  # Turn priority:
  # Match Number with Numbered Card (not using same colour)
  # Match Type with Special Coloured Card (not using same colour)
  # Wild/+4
  # Match Colour with Numbered Card
  # Match Colour with Special Coloured Card
  # Draw
  def turn(self, hand, lastDiscard): # Choosing discard. No need to check validity of move since logic is in method
    for i in range(len(hand)):
      if(hand[i].type == lastDiscard.type and hand[i].colour != lastDiscard.colour and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].type == lastDiscard.type and hand[i].colour != lastDiscard.colour):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == "wild"):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour):
        return i
    return "draw"
  # Colour select:
  # Select the most common colour in hand that is not the same as the last colour
  # If hand is all wilds, select random colour
  def colourselect(self, hand, lastDiscard): # Choosing colour after using wild
    listForConvenience = []
    for i in hand:
      if(i.colour == "wild" or i.colour == lastDiscard.colour):
        continue
      listForConvenience.insert(len(listForConvenience), i.colour)
    if(len(listForConvenience) == 0):
      return deckColourInput[random.randint(0, 3)]
    return mode(listForConvenience)

class Andy(Player): # Andy is between Mandy and Nancy. He will always try to match a number first, otherwise he plays like Mandy
  name = "Andy"
  # Turn priority:
  # Match Number with Numbered Card
  # Match Colour with Numbered Card
  # Match Colour/Type with Special Coloured Card
  # Wild/+4
  # Draw
  def turn(self, hand, lastDiscard): # Choosing discard. No need to check validity of move since logic is in method
    for i in range(len(hand)):
      if(hand[i].type == lastDiscard.type and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour and hand[i].type.isdigit()):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == lastDiscard.colour or hand[i].type == lastDiscard.type):
        return i
    for i in range(len(hand)):
      if(hand[i].colour == "wild"):
        return i
    return "draw"
  # Colour select:
  # Select the most common colour in hand
  # If hand is all wilds, select random colour
  def colourselect(self, hand, lastDiscard): # Choosing colour after using wild
    listForConvenience = []
    for i in hand:
      if(i.colour == "wild"):
        continue
      listForConvenience.insert(len(listForConvenience), i.colour)
    if(len(listForConvenience) == 0):
      return deckColourInput[random.randint(0, 3)]
    return mode(listForConvenience)
  

class MegaBot(Player):
  name = "MegaBot"

  engines = [Mandy("MandyEngine"), Andy("AndyEngine"), Nancy("NancyEngine")]
  engineIndexes = [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0]

  def turn(self, hand, lastDiscard, allHands):
    engine = len(hand)
    if(engine > 10):
      engine = 10
    engine = self.engineIndexes[engine]
    
    for i in allHands:
      if(len(i) <= 2 and i != hand):
        for j in range(len(hand)):
          if(hand[j].type == "+" or hand[j].type == "f" or hand[j].type == "s"):
            if(turncheck(hand[j], lastDiscard)):
              return j

    return self.engines[engine].turn(hand, lastDiscard)
  
  def colourselect(self, hand, lastDiscard):
    engine = len(hand)
    if(engine > 10):
      engine = 10
    engine = self.engineIndexes[engine]

    return self.engines[engine].colourselect(hand, lastDiscard)


# Make a list of players
#players = [Mandy("Mandy"), Nancy("Nancy"), Andy("Andy"), Randy("Randy"), MegaBot("MegaBot")]
#players = [Mandy("Mandy"), Mandy("Mandy1"), Mandy("Mandy2"), Mandy("Mandy3"), MegaBot("MegaBot")]
#players = [Mandy("Mandy"), Mandy("Mandy1"), Mandy("Mandy2"), Mandy("Mandy3"), Andy("Andy")]
#players = [Player("USER"), MegaBot("MegaBot")]

if __name__ == "__main__":
  deck = Deck()
  discard = []
  players = [Mandy("Mandy"), Nancy("Nancy"), Andy("Andy"), Randy("Randy")]

  for i in tqdm(range(100)): # Play n games
    startGame(players, deck, discard)

  for i in players: # Print win stats
    print(i.name + " wins: " + str(i.wins))