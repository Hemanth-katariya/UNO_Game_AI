# game/card.py

class Card:
    def __init__(self, color, value):
        self.color = color  # Red, Blue, Green, Yellow, or None for wild
        self.value = value  # 0-9, Skip, Reverse, Draw Two, Wild, Wild Draw Four

    def is_playable_on(self, top_card):
        return (self.color == top_card.color or
                self.value == top_card.value or
                self.color is None or  # Wild
                top_card.color is None)

    def __repr__(self):
        return f"{self.color} {self.value}"
