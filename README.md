# ♠️ UNO_AI - Intelligent UNO Game

Welcome to **UNO_AI**, a smart and fun Python-based implementation of the UNO card game, where Artificial Intelligence meets the colorful world of cards 🎴. Built by a team of passionate developers, this game lets you play against two types of AI agents: a Rule-Based agent and a Monte Carlo Tree Search (MCTS) agent.

---

## 🚀 Features

- 🧠 **AI Agents** – Rule-Based & MCTS AI strategies
- 🧍‍♀️ **Human vs AI** – Play against intelligent bots
- 🎨 **Pygame Interface** – Smooth graphical gameplay
- ♻️ **Full UNO Support** – Reverse, Skip, Wild, Draw Two/Four cards
- 💡 **Modular Codebase** – Easy to extend or upgrade
- 🎮 **Simple Setup** – Just Python + Pygame!

---

## 🧠 AI Agents

| Agent          | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `HumanPlayer`  | Allows human input to play cards manually                                  |
| `RuleBased`    | Follows fixed rules and heuristics to make strategic plays                 |
| `MCTSAgent`    | Uses **Monte Carlo Tree Search** to simulate possible future game states   |

---

## 🗂️ Project Structure

```bash
UNO_AI/
├── main.py                 # Entry point to start the game
├── README.md               # Project documentation
│
├── agents/                 # AI players and human player
│   ├── human_player.py     # Logic for human input
│   ├── mcts_agent.py       # Monte Carlo Tree Search agent
│   └── rule_based.py       # Rule-based agent using fixed heuristics
│
├── game/                   # Core UNO game components
│   ├── card.py             # Card class and card types
│   ├── deck.py             # Deck creation and shuffling logic
│   ├── player.py           # Player logic and card handling
│   └── uno_game.py         # Game loop and main mechanics
│
├── ui/                     # Display and rendering
│   └── display.py          # Pygame-based visual interface
```
---
## Installation
```bash
git clone https://github.com/your-username/UNO_AI.git
cd UNO_AI
pip install -r requirements.txt
python main.py
```





