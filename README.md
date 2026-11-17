# Wilderness Survival System

A text-based wilderness survival game written in Python for CS 3560 (Object-Oriented Programming). The player crosses a randomly generated map of terrain, managing food, water, movement points, and gold, and haggling with traders along the way.

## Running the game

Requires Python 3. There are no third-party dependencies.

```bash
python WSS.py
```

You will be asked for a map width, a height, and a difficulty (`easy`, `medium`, or `hard`). The game then generates the map and prints it using emojis:

| Terrain  | Emoji |
|----------|-------|
| Plains   | 🌱 |
| Forest   | 🌲 |
| Swamp    | 🐊 |
| Desert   | 🏜️ |
| Mountain | ⛰️ |

## Project structure

| File | Contents |
|------|----------|
| [WSS.py](WSS.py) | Entry point. Reads the map settings from the user and displays the map. |
| [map.py](map.py) | `GameMap`: builds a grid of random terrain weighted by difficulty. |
| [terrain.py](terrain.py) | `Terrain` and its subclasses `Plains`, `Forest`, `Swamp`, `Mountain`, `Desert`. |
| [item.py](item.py) | `Item` and its subclasses `Food`, `Water`, `Gold`. |
| [trader.py](trader.py) | `Trader` and its subclasses `GrumpyTrader`, `FickleTrader`, `FriendlyTrader`, plus the trade data types. |
| [player.py](player.py) | `Player`: the player's name, inventory, and stats. |

## How it works

### Map generation

Harder difficulties produce more of the expensive terrain types:

| Difficulty | Plains | Forest | Swamp / Desert / Mountain |
|------------|--------|--------|---------------------------|
| Easy       | 60%    | 25%    | 15% |
| Medium     | 35%    | 25%    | 40% |
| Hard       | 15%    | 20%    | 65% |

### Terrain

Entering a square costs water, food, and movement points. Staying in a square to rest costs half the water and food, and gives back 2 movement points.

| Terrain  | Water | Food | Movement |
|----------|-------|------|----------|
| Plains   | 1 | 1 | 1 |
| Forest   | 1 | 2 | 2 |
| Swamp    | 1 | 3 | 3 |
| Desert   | 3 | 2 | 2 |
| Mountain | 3 | 3 | 4 |

Each square can hold up to three resources (one water source, one gold nugget, one food), and each has a 50% chance to appear. Gold is removed once collected. Repeatable resources, such as River Water, stay in the square so the player can collect them again.

### Traders

Every square has a trader who swaps gold, water, and food. All traders look the same to the player, but each type has a different personality:

- **Trader**: asks for a small profit on every trade and makes a few counter-offers before giving up.
- **GrumpyTrader**: wants a large margin, has little patience, and walks away from lowball offers.
- **FickleTrader**: re-rolls the margin it wants on every offer.
- **FriendlyTrader**: very patient, and lowers its margin with each counter-offer.

A trader who has made a deal, or who has lost patience, won't trade again for a few turns.

## Status

Work in progress. Map generation and display, terrain, items, and traders are in place. The player and the main game loop (movement, collecting, trading) are still being built.
