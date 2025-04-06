# game/player.py

class Player:
    def __init__(self, name, agent):
        self.name = name
        self.hand = []
        self.agent = agent  # AI or rule-based logic

    def draw_card(self, deck, num=1):
        self.hand.extend(deck.draw(num))

    def play_turn(self, top_card, color_choice, game_state):
        playable = [card for card in self.hand if card.is_playable_on(top_card)]

        card_to_play, declared_color = self.agent.select_card(
            self.hand, top_card, playable, color_choice, game_state
        )

        if card_to_play:
            self.hand.remove(card_to_play)
            return card_to_play, declared_color
        else:
            return None, None

    def has_won(self):
        return len(self.hand) == 0

    def __repr__(self):
        return f"{self.name} ({len(self.hand)} cards)"
