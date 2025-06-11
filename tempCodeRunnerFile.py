# import pygame
# from game.player import Player
# from agents.mcts_agent import MCTSAgent
# from agents.rule_based import RuleBasedAgent
# from agents.human_player import HumanPlayer
# from game.uno_game import UNOGame
# from ui.display import show_winner_screen, draw_menu

# def main():
#     pygame.init()
    
#     # Show welcome screen and get game mode
#     mode = draw_menu()
    
#     # Create players based on selected mode
#     if mode == 1:  # AI vs AI
#         player1 = Player("MCTSBot", MCTSAgent("MCTSBot", simulations=50))
#         player2 = Player("RuleBot", RuleBasedAgent("RuleBot"))
#         players = [player1, player2]
#     elif mode == 2:  # Human vs AI
#         player1 = HumanPlayer("You")
#         player2 = Player("AI", MCTSAgent("AI", simulations=30))
#         players = [player1, player2]
#     elif mode == 3:  # Human vs Human
#         player1 = HumanPlayer("Player 1")
#         player2 = HumanPlayer("Player 2")
#         players = [player1, player2]
#     elif mode == 4:  # Tournament mode
#         player1 = Player("MCTS Pro", MCTSAgent("MCTS Pro", simulations=100))
#         player2 = Player("RuleMaster", RuleBasedAgent("RuleMaster"))
#         player3 = HumanPlayer("Human")
#         players = [player1, player2, player3]
    
#     # Create and run game
#     game = UNOGame(players)
#     game.run()
#     show_winner_screen(game.winner.name)

# if __name__ == "__main__":
#     main()