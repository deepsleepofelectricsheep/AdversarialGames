from dataclasses import dataclass
from typing import Tuple, Any
import random


@dataclass(frozen=True)
class State:
    # Basic state definition for Quoridor game
    p1: Tuple[int, int] # (x, y)
    p2: Tuple[int, int]
    p1_numwalls: int
    p2_numwalls: int
    turn: int
    h_walls: frozenset
    v_walls: frozenset

    def __lt__(self, other) -> bool: # To prevent errors later
        return True
    

class Quoridor:
    def __init__(self, size=5, numwalls=3) -> None:
        self.size = size
        self.numwalls = numwalls
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # Precompute valid wall positions
        self.wall_placement_candidates = [
            (i, j) for i in range(self.size - 1) for j in range(self.size - 1)
        ]

    def start_state(self) -> State:
        mid = self.size // 2
        return State(
            p1=(mid, 0),
            p2=(mid, self.numwalls-1),
            p1_numwalls=self.numwalls,
            p2_numwalls=self.numwalls,
            turn=1,
            h_walls=frozenset(),
            v_walls=frozenset()
        )
    
    def is_end(self, state: State) -> bool:
        return True if state.p1[1]==self.size-1 or state.p2[1]==0 else False
    
    def utility(self, state: State) -> float:
        return 1 if state.p1[1]==self.size-1 else -1 if state.p2[1]==0 else 0
    
    def _hop_straight(self, direction: Tuple[int, int]) -> Tuple[int, int]:
        if direction == (0, 1):
            return (0, 2)
        if direction == (0, -1):
            return (0, -2)
        if direction == (1, 0):
            return (2, 0)
        if direction == (-1, 0):
            return (-2, 0)
        
    def _hop_diagonally(self, direction: Tuple[int, int]) -> list[Tuple[int, int]]:
        if direction == (0, 1):
            return [(1, 1), (-1, 1)]
        if direction == (0, -1):
            return [(1, -1), (-1, -1)]
        if direction == (1, 0):
            return [(1, 1), (1, -1)]
        if direction == (-1, 0):
            return [(-1, 1), (-1, -1)]      

    def _is_blocked(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]]) -> bool:
        return False
    
    def _path_exists(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]]) -> bool:
        return True
    
    def _get_pawn_moves(self, state: State) -> list[Tuple[int, int]]:

        legal_pawn_moves = []

        # Happy path: orthogonal square is within bounds and neither blocked nor occupied by opponent
        for direction in self.directions:
            successor = self.successor(state, ('pawn', direction))
            if successor.p1 != successor.p2:
                if successor.p1 < (self.size, self.size) and successor.p2 < (self.size, self.size):
                    if state.turn == 1:
                        if not self.is_blocked(state.p1, successor.p1, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)
                    elif state.turn == 2:
                        if not self.is_blocked(state.p2, successor.p2, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)      

        # Unhappy path: orthogonal square is occupied by opponent
        for direction in self.directions:
            successor = self.successor(state, ('pawn', direction))
            if successor.p1 == successor.p2:
                # First, try hopping straight
                failed = True
                hop = self._hop_straight(direction)
                successor = self.successor(state, ('pawn', hop))
                if successor.p1 < (self.size, self.size) and successor.p2 < (self.size, self.size):
                    if state.turn == 1:
                        if not self.is_blocked(state.p1, successor.p1, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)
                            failed = False
                    elif state.turn == 2:
                        if not self.is_blocked(state.p2, successor.p2, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)
                            failed = False

                # Next, try hopping diagonally
                if failed:
                    for hop in self._hop_diagonally(direction):
                        successor = self.successor(state, ('pawn', hop))
                        if successor.p1 < (self.size, self.size) and successor.p2 < (self.size, self.size):
                            if state.turn == 1:
                                if not self.is_blocked(state.p1, successor.p1, state.h_walls, state.v_walls):
                                    legal_pawn_moves.append(direction)
                            elif state.turn == 2:
                                if not self.is_blocked(state.p2, successor.p2, state.h_walls, state.v_walls):
                                    legal_pawn_moves.append(direction)

        return legal_pawn_moves
    
    def _get_h_wall_placements(self, state: State) -> list[Tuple[int, int]]:
        
        legal_placements = []

        for candidate in self.wall_placement_candidates:
           if candidate not in state.h_walls:
               successor = self.successor(state, ('h_wall', candidate))
               if self._path_exists(successor.p1, successor.p2, successor.h_walls, successor.v_walls):
                   legal_placements.append(candidate)

        return legal_placements
    
    def _get_v_wall_placements(self, state: State) -> list[Tuple[int, int]]:
        
        legal_placements = []

        for candidate in self.wall_placement_candidates:
           if candidate not in state.v_walls:
               successor = self.successor(state, ('v_wall', candidate))
               if self._path_exists(successor.p1, successor.p2, successor.h_walls, successor.v_walls):
                   legal_placements.append(candidate)

        return legal_placements  

    def actions(self, state: State) -> list[Tuple[str, Any]]:
        actions = []
        # Pawn moves
        pawn_moves = self._get_pawn_moves(state) 
        for pawn_move in pawn_moves:
            actions.append(('pawn', pawn_move))
        # Horizontal wall placements
        h_wall_placements = self._get_h_wall_placements(state)
        for h_wall_placement in h_wall_placements:
            actions.append(('h_wall', h_wall_placement))
        # Vertical wall placements
        v_wall_placements = self._get_v_wall_placements(state)
        for v_wall_placement in v_wall_placements:
            actions.append(('v_wall', v_wall_placement))
        return actions
    
    def successor(self, state: State, action: Tuple[str, Any]) -> State:
        move_type, move = action
        # Move was a pawn move
        if move_type == 'pawn':
            return State(
                p1=(state.p1[0]+move[0], state.p1[1]+move[1]) if state.turn==1 else state.p1,
                p2=(state.p2[0]+move[0], state.p2[1]+move[1]) if state.turn==2 else state.p2,
                turn=1 if state.turn==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls,
                p2_numwalls=state.p2_numwalls,
                h_walls=state.h_walls,
                v_walls=state.v_walls
            )
        # Move was a h_wall placement
        if move_type == 'h_wall':
            h_walls = [h_wall for h_wall in state.h_walls]
            h_walls.append(move)
            return State(
                p1=state.p1,
                p2=state.p2,
                turn=1 if state.turn==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls-1 if state.turn==1 else state.p1_numwalls,
                p2_numwalls=state.p2_numwalls-1 if state.turn==2 else state.p2_numwalls,
                h_walls=frozenset(h_walls),
                v_walls=state.v_walls
            )
        # Move was a v_wall placement
        if move_type == 'v_wall':
            v_walls = [v_wall for v_wall in state.v_walls]
            v_walls.append(move)
            return State(
                p1=state.p1,
                p2=state.p2,
                turn=1 if state.turn==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls-1 if state.turn==1 else state.p1_numwalls,
                p2_numwalls=state.p2_numwalls-1 if state.turn==2 else state.p2_numwalls,
                h_walls=state.h_walls,
                v_walls=frozenset(v_walls)
            )
        # Unknown move type
        else: 
            raise ValueError("Invalid move type.")
        
    def visualize(self, state: State) -> None:
        #TODO: Implement method to visualize Quoridor board, complete with row and column labels.
        raise NotImplementedError()