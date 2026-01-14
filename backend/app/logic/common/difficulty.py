"""
Definește constante pentru configurarea dificultății problemelor generate.
"""

# Configurații pentru L6 (MinMax)
MINMAX_L6_MIN_DEPTH = 0
MINMAX_L6_MAX_DEPTH = 5

MINMAX_L6_MIN_BREADTH = 1
MINMAX_L6_MAX_BREADTH = 3

# Nash
NASH_MATRIX_MIN_SIZE = 2
NASH_MATRIX_MAX_SIZE = 3

NASH_MIN_PAYOFF = -5
NASH_MAX_PAYOFF = 10

# Reinforcement Learning
RL_GRID_MIN_ROWS = 3
RL_GRID_MAX_ROWS = 4
RL_GRID_MIN_COLS = 3
RL_GRID_MAX_COLS = 4

RL_DEFAULT_GAMMA = 0.9
RL_DEFAULT_STEP_REWARD = -0.04
RL_DEFAULT_ALPHA = 0.1 # Learning rate