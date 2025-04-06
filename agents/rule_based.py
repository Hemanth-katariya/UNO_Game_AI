from game.player import Player
from collections import Counter
import random

class RuleBasedAgent(Player):
    def __init__(self, name="RuleBot"):
        super().__init__(name, self)
        self.priority_map = {
            None: 0,  # Wild cards
            'Draw Two': 3,
            'Skip': 3,
            'Reverse': 3,
            'Wild Draw Four': 4,
            'Wild': 1
        }

    def select_card(self, hand, top_card, playable_cards, current_color, game_state):
        if not playable_cards:
            return None, None

        # Get card with highest priority
        best_card = max(playable_cards, key=lambda c: self.priority_map.get(c.value, 2))

        # Choose color for wild cards
        if best_card.color is None:
            colors = [card.color for card in hand if card.color]
            if colors:
                chosen_color = Counter(colors).most_common(1)[0][0]
            else:
                chosen_color = random.choice(['Red', 'Green', 'Blue', 'Yellow'])
        else:
            chosen_color = best_card.color

        return best_card, chosen_color