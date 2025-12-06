from games.quoridor import Quoridor
from agents.minimax import MiniMax
from agents.random import RandomAgent
import argparse


def initialize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    # Add player choice arguments
    parser.add_argument('-p1', '--player_1', type=str, 
                        help='choice of player 1', 
                        options=['Quoridor', 'MiniMax', 'RandomAgent']
    )