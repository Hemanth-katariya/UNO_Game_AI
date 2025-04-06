# uno_game.py
import random
import pygame  # Required for time delay
from game.deck import Deck
from game.player import Player # Make sure HumanPlayer is defined in player module
from agents.human_player import HumanPlayer
from ui.display import show_turn

class UNOGame:
    def __init__(self, players):
        self.deck = Deck()
        self.discard_pile = []
        self.players = players
        self.current_index = 0
        self.direction = 1  # 1: clockwise, -1: counter-clockwise
        self.current_color = None
        self.skip_next = False
        self.winner = None

    def setup(self):
        for player in self.players:
            player.draw_card(self.deck, 7)

        first_card = self.deck.draw(1)[0]
        while first_card.value in ['Wild', 'Wild Draw Four']:
            self.deck.cards.append(first_card)
            random.shuffle(self.deck.cards)
            first_card = self.deck.draw(1)[0]

        self.discard_pile.append(first_card)
        self.current_color = first_card.color
        self.apply_action(first_card)

    def next_player_index(self):
        return (self.current_index + self.direction) % len(self.players)

    def apply_action(self, card):
        if card.value == 'Skip':
            self.skip_next = True
        elif card.value == 'Reverse':
            self.direction *= -1
        elif card.value == 'Draw Two':
            self.players[self.next_player_index()].draw_card(self.deck, 2)
            self.skip_next = True
        elif card.value == 'Wild Draw Four':
            self.players[self.next_player_index()].draw_card(self.deck, 4)
            self.skip_next = True

    def play_turn(self):
        player = self.players[self.current_index]
        top_card = self.discard_pile[-1]

        show_turn(player.name, top_card, player.hand)

        # Add small delay for AI turns so humans can follow
        if not isinstance(player, HumanPlayer):
            pygame.time.delay(1000)  # 1 second delay for AI moves

        card, declared_color = player.play_turn(top_card, self.current_color, self.get_state_snapshot())

        if card:
            self.discard_pile.append(card)
            self.current_color = declared_color if card.color is None else card.color
            self.apply_action(card)
            print(f"{player.name} played: {card}")
        else:
            player.draw_card(self.deck)
            print(f"{player.name} drew a card")

        if player.has_won():
            self.winner = player
            return

        self.current_index = self.next_player_index()
        if self.skip_next:
            print(f"{self.players[self.current_index].name} is skipped!")
            self.current_index = self.next_player_index()
            self.skip_next = False

    def run(self):
        print("\U0001F308 Starting UNO Game!\n")
        self.setup()
        while not self.winner:
            self.play_turn()

        print(f"\n🏆 {self.winner.name} wins the game!")

    def get_game_state(self):
        return {
            'player_count': len(self.players),
            'discard_top': self.discard_pile[-1],
            'current_color': self.current_color,
            'direction': self.direction,
            'deck': self.deck,  # must be deepcopy-able
            'discard_pile': self.discard_pile[:],  # current discard stack
        }

    def get_state_snapshot(self):
        return {
            'player_count': len(self.players),
            'discard_top': self.discard_pile[-1],
            'current_color': self.current_color,
            'direction': self.direction,
        }
