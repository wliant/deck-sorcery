# Hearthstone Genetic Algorithm Deck Generator

## Overview

This project implements a genetic algorithm to generate optimal card decks for a given hero class in the Hearthstone card game. The algorithm takes into account various constraints and aims to maximize the deck's performance based on predefined rules and predictions.

## Implementation Details

### Key Components

1. **DataProvider.py**:
   - `getLibrary()`: Retrieves and sorts the library of cards.
   - `getAssociationRules(heroClass)`: Fetches association rules for a given hero class.
   - `getLibraryCardIdsForConstruction(heroClass)`: Gets card IDs for deck construction based on the hero class.

2. **GA.py**:
   - `GeneticAlgorithm`: Class implementing the genetic algorithm.
     - `__init__`: Initializes the genetic algorithm with the hero class, initial selection, and card pool.
     - `evalFct`: Evaluates the fitness of an individual deck.
     - `feasible`: Checks if a deck is feasible based on card rarity constraints.
     - `run`: Runs the genetic algorithm to evolve the population and find the optimal deck.
   - `generateDeck(heroClass, initialSelection, useLibrary)`: Function to generate a deck using the genetic algorithm.

### Dependencies

- `deap`: Distributed Evolutionary Algorithms in Python.
- `random`: Python's built-in module for generating random numbers.
- `time`: Python's built-in module for time-related functions.

## How to Run

1. **Install Dependencies**:
   Ensure you have Python installed. Install the required packages using pip:
   ```sh
   pip install deap