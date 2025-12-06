from agents.base import Agent
from typing import Any, Tuple


class MiniMax(Agent):
    def __init__(self, game: Any, name: str = 'MiniMax', turn: int = 1, depth: int = 2) -> None:
        self.game = game
        self.name = name
        self.turn = turn
        self.depth = depth

    def action(self, state: Any) -> Any:
        best_value, best_action = self._minimax(state, self.depth, float('-inf'), float('inf'))
        return best_action
    
    def _minimax(self, state: Any, depth: int, a: float, b: float) -> Tuple[float, Any]:

        # Base case #1: game over
        if self.game.is_end(state):
            return self.game.utility(state), None
        
        # Base case #2: max depth reached
        if depth == 0:
            return self._evaluate(state), None
        
        # Recursive case
        # Max agent
        if state.turn == self.turn:
            best_value, best_action = float('-inf'), None
            actions = self.game.actions(state)
            for action in actions:
                successor = self.game.successor(state, action)
                successor_value, successor_action = self._minimax(successor, depth, a, b)
                if successor_value > best_value:
                    best_value = successor_value
                    best_action = action
                if best_value > b:
                    break
                a = max(a, best_value)
            return best_value, best_action                
        # Min agent
        else:
            worst_value, worst_action = float('+inf'), None
            actions = self.game.actions(state)
            for action in actions: 
                successor = self.game.successor(state, action)
                successor_value, successor_action = self._minimax(successor, depth-1, a, b)
                if successor_value < worst_value:
                    worst_value = successor_value
                    worst_action = action   
                if worst_value < a:
                    break
                a = min(b, worst_value)
            return worst_value, worst_action
        
    def _evaluate(self, state: Any) -> float:
        return 0