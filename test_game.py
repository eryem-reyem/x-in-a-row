import game
import pytest

def trim_board(ascii_board):
    return '\n'.join([i.strip() for i in ascii_board.splitlines()])
t = trim_board

def test_new_board():
    game.Board(3,3).ascii() == t("""
    ...
    ...
    ...
    """)

    game.Board(4,3).ascii() == t("""
    ....
    ....
    ....
    """)

    game.Board(3,4).ascii() == t("""
    ...
    ...
    ...
    ...
    """)

def test_game():
    board = game.Board(3,3,win=3)
    assert board.count_tokens == 0
    assert board.game_status == 'active'
    assert board.turn_color == None
    # drop first token
    token = board.drop('x',0)
    assert board.game_status == 'active'
    assert token.position == (0,0)
    assert token.color == 'x'
    assert board.ascii() == t("""
    ...
    ...
    x..
    """)
    assert board.count_tokens == 1
    assert board.turn_color == 'o'
    # drop second token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,1)
    assert token.color == 'o'
    assert board.ascii() == t("""
    ...
    o..
    x..
    """)
    assert board.count_tokens == 2
    assert board.turn_color == 'x'

    # dropping the wrong color should raise an error
    with pytest.raises(Exception):
        token = board.drop('o',1)

    # drop third token
    token = board.drop('x',1)
    assert board.game_status == 'active'
    assert token.position == (1,0)
    assert token.color == 'x'
    board.ascii() == t("""
    ...
    o..
    xx.
    """)
    assert board.count_tokens == 3
    assert board.turn_color == 'o'
    # drop fourth token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,2)
    assert token.color == 'o'
    board.ascii() == t("""
    o..
    o..
    xx.
    """)
    assert board.count_tokens == 4
    # drop fifth token
    token = board.drop('x',2)
    assert board.game_status == 'over'
    assert board.won_by == 'x'
    assert token.position == (2,0)
    assert token.color == 'x'
    board.ascii() == t("""
    o..
    o..
    xxx
    """)
    assert board.count_tokens == 5

def test_game_2():
    board = game.Board(5,5,win=3)
    assert board.count_tokens == 0
    assert board.game_status == 'active'
    assert board.turn_color == None
    # drop first token
    token = board.drop('x',0)
    assert board.game_status == 'active'
    assert token.position == (0,0)
    assert token.color == 'x'
    assert board.ascii() == t("""
    .....
    .....
    .....
    .....
    x....
    """)
    assert board.count_tokens == 1
    assert board.turn_color == 'o'
    # drop second token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,1)
    assert token.color == 'o'
    assert board.ascii() == t("""
    .....
    .....
    .....
    o....
    x....
    """)
    assert board.count_tokens == 2
    assert board.turn_color == 'x'

    # dropping the wrong color should raise an error
    with pytest.raises(Exception):
        token = board.drop('o',1)

    # drop third token
    token = board.drop('x',1)
    assert board.game_status == 'active'
    assert token.position == (1,0)
    assert token.color == 'x'
    board.ascii() == t("""
    .....
    .....
    .....
    o....
    xx...
    """)
    assert board.count_tokens == 3
    assert board.turn_color == 'o'
    # drop fourth token
    token = board.drop('o',0)
    assert board.game_status == 'active'
    assert token.position == (0,2)
    assert token.color == 'o'
    board.ascii() == t("""
    .....
    .....
    o....
    o....
    xx...
    """)
    assert board.count_tokens == 4
    # drop fifth token
    token = board.drop('x',2)
    assert board.game_status == 'over'
    assert board.won_by == 'x'
    assert token.position == (2,0)
    assert token.color == 'x'
    board.ascii() == t("""
    .....
    .....
    o....
    o....
    xxx..
    """)
    assert board.count_tokens == 5

def test_load_board():
    """
    The Board class should provide a load method to load a predefined board.
    the load method should be implemented as a static method like this:

    >>> class Test:
    >>>     @staticmethod
    >>>     def a_static_factory():
    >>>        t = Test()
    >>>        # do something with t and return it
    >>>        return t

    the load function accepts a board layout. It retrieves the dimensions of the board
    and loads the provided data into the board.
    """

    board = game.Board.load(t("""
    o..
    o..
    xxx
    """))

def test_axis_strings():
    board = game.Board.load(t("""
    o..
    o..
    xxx
    """))

    # get the axis strings in this order:  | \ / -
    axis_strings = board.axis_strings(0,0)
    assert axis_strings[0] == 'xoo'
    assert axis_strings[1] == 'x'
    assert axis_strings[2] == 'x..'
    assert axis_strings[3] == 'xxx' # the winner :-)

def test_check_win():
    board = game.Board.load(t("""
    .....
    .....
    .....
    xx...
    xooo.
    """))
    assert board.count_tokens == 0
    assert board.game_status == 'active'
    assert board.turn_color == None
    # drop first token
    token = board.drop('o', 4)
    assert board.game_status == 'over'
    assert board.won_by == 'o'
    assert token.position == (4,0)
    assert token.color == 'o'
    board.ascii() == t("""
    .....
    .....
    .....
    xx...
    xoooo
    """)
    assert board.count_tokens == 1

def test_check_win_2():
    board = game.Board.load(t("""
    .....
    .....
    .....
    xx...
    xoo.o
    """))
    assert board.count_tokens == 0
    assert board.game_status == 'active'
    assert board.turn_color == None
    # drop first token
    token = board.drop('o', 3)
    assert board.game_status == 'over'
    assert board.won_by == 'o'
    assert token.position == (3,0)
    assert token.color == 'o'
    board.ascii() == t("""
    .....
    .....
    .....
    xx...
    xoooo
    """)
    assert board.count_tokens == 1
