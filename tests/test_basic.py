from games.quoridor import State as QuoridorState
from games.quoridor import Quoridor


def simple():
    # Does the game return the correct start state? 
    game = Quoridor(size=3, numwalls=3)
    start_state = game.start_state()
    expected_start_state = QuoridorState(
        p1=(1, 0), 
        p2=(1, 2), 
        p1_numwalls=3, 
        p2_numwalls=3,
        turn=1,
        h_walls=frozenset(),
        v_walls=frozenset()
    )
    if expected_start_state.p1 != start_state.p1:
        print('Start position of player 1 not correct')
    if expected_start_state.p2 != start_state.p2:
        print('Start position of player 2 not correct')
    # Does the game return the correct legal moves for a simple start position?
    actions = game.actions(start_state)
    pawn_moves = [move for typ, move in actions if typ == 'pawn']
    expected_pawn_moves = [(1, 0), (-1, 0), (0, 1)]
    for pawn_move in pawn_moves:
        if pawn_move not in expected_pawn_moves:
            print('Simple pawn moves test failed. '
                  f'Got unexpected pawn move from starting position: {pawn_move}.')
    # Do the pawn moves result in the correct successors? 


if __name__ == '__main__':
    simple()