import random
import time
from collections import defaultdict
from game.player import Player
from agents.rule_based import RuleBasedAgent

class MCTSAgent(Player):
    def __init__(self, name="MCTSBot", simulations=50, max_time=1.0):
        super().__init__(name, self)
        self.name = name
        self.simulations = simulations
        self.max_time = max_time
        self.rule_based = RuleBasedAgent(name + "_Helper")

    def select_card(self, hand, top_card, playable_cards, current_color, game_state):
        if not playable_cards:
            return None, None

        # Early exit for single option
        if len(playable_cards) == 1:
            return self._choose_color(playable_cards[0], hand)

        win_counts = defaultdict(int)
        start_time = time.time()
        sim_count = 0                   
        
        # Time-limited simulations
        while time.time() - start_time < self.max_time and sim_count < self.simulations:
            for card in playable_cards:
                result = self.simulate(card, hand.copy(), current_color, game_state.copy())
                if result == self.name:
                    win_counts[card] += 1
                sim_count += 1
                if time.time() - start_time >= self.max_time:
                    break

        if not win_counts:  # No wins recorded, fallback to rule-based
            return self.rule_based.select_card(hand, top_card, playable_cards, current_color, game_state)

        # Select card with highest win count
        best_card = max(win_counts.items(), key=lambda x: x[1])[0]
        return self._choose_color(best_card, hand)

    def simulate(self, card, hand, current_color, game_state):
        # Simplified simulation - in a real implementation, this would play out a full game
        # For now, we'll just return a random winner
        return random.choice([self.name, "Opponent"])

    def _choose_color(self, card, hand):
        if card.color is None:  # Wild card
            colors = [c.color for c in hand if c.color]
            if colors:
                chosen_color = max(set(colors), key=colors.count)
            else:
                chosen_color = random.choice(['Red', 'Green', 'Blue', 'Yellow'])
            return card, chosen_color
        return card, card.color