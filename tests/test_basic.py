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
    action = (0, 1)
    successor = game.successor(start_state, ('pawn', action))
    expected_p1 = (expected_start_state.p1[0] + action[0], expected_start_state.p1[1] + action[1])
    if successor.p1 != expected_p1 or successor.p2 != expected_start_state.p2:
        print('The wrong successor was generated.')

    # Are invalid actions, such as those requiring a wall jump, generated? 
    state = QuoridorState(
        p1=(1, 0), 
        p2=(1, 2), 
        p1_numwalls=0, 
        p2_numwalls=0,
        turn=1,
        h_walls=frozenset([(1, 0)]),
        v_walls=frozenset()
    )
    actions = game.actions(state)
    expected_actions = [('pawn', (1, 0)), ('pawn', (-1, 0))]
    for action in actions:
        if action not in expected_actions:
            print('The following invalid action was generated for player 1 '
                  f'if a h_wall is placed at (1, 0): {action}')

    state = QuoridorState(
        p1=(1, 0), 
        p2=(1, 2), 
        p1_numwalls=0, 
        p2_numwalls=0,
        turn=1,
        h_walls=frozenset(),
        v_walls=frozenset([(1, 0)])
    )
    actions = game.actions(state)
    expected_actions = [('pawn', (-1, 0)), ('pawn', (0, 1))]
    for action in actions:
        if action not in expected_actions:
            print('The following invalid action was generated for player 1 '
                  f'if a v_wall is placed at (1, 0): {action}')
            
    # If the two pawns are orthoginally adjacent, are hop straight moves generated appropriately?
    state = QuoridorState(
        p1=(1, 0), 
        p2=(1, 1), 
        p1_numwalls=0, 
        p2_numwalls=0,
        turn=1,
        h_walls=frozenset(),
        v_walls=frozenset()
    )
    actions = game.actions(state)
    expected_action = ('pawn', (0, 2))
    if expected_action not in actions:
        print('The correct hop straight move was not generated')
        print(actions)

    # Manual check: Does the visualized board look right?
    game = Quoridor(size=5, numwalls=3)
    state = QuoridorState(
        p1=(1, 0), 
        p2=(1, 1), 
        p1_numwalls=0, 
        p2_numwalls=0,
        turn=1,
        h_walls=frozenset([(1, 0)]),
        v_walls=frozenset([(2, 1)])
    )
    game.visualize(state)


if __name__ == '__main__':
    simple()