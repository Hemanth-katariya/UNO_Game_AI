# game/deck.py

import random
from game.card import Card

class Deck:
    COLORS = ['Red', 'Green', 'Blue', 'Yellow']
    VALUES = [str(n) for n in range(0, 10)] + ['Skip', 'Reverse', 'Draw Two']
    WILD_CARDS = ['Wild', 'Wild Draw Four']

    def __init__(self):
        self.cards = self.generate_full_deck()
        random.shuffle(self.cards)

    def generate_full_deck(self):
        deck = []
        for color in self.COLORS:
            for value in self.VALUES:
                deck.append(Card(color, value))
                if value != '0':  # Two of each except 0
                    deck.append(Card(color, value))
        for wild in self.WILD_CARDS:
            for _ in range(4):
                deck.append(Card(None, wild))
        return deck

    def draw(self, num=1):
        drawn = self.cards[:num]
        self.cards = self.cards[num:]
        return drawn

    def is_empty(self):
        return len(self.cards) == 0
