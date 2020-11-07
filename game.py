class Board: 
    DIRECTIONS = ((1 ,0), (1, -1), (1, 1), (0, 1), (-1, 0), (-1, 1), (-1, -1), (0, -1))
    def __init__(self, width, height, win=4):
        self.width = width
        self.height = height
        self.win = win
        self.board = [['.' for x in range(self.width)]
                      for y in range(self.height)]
        self.count_tokens = 0
        self.game_status = 'active'
        self.turn_color = None
        self.lines = []
        for line in range(self.width):
            self.lines.append(0)
        self.position = []
        self.won_by = None
        
    def ascii(self):
        out=['']
        for i in range(len(self.board)):
            out.append((''.join(self.board[len(self.board)-i-1])))
        out.append('')
        return '\n'.join(out)

    def choose_player(self):
        self.turn_color = input('Star with x or o? Please choose_ ')
        if self.turn_color == 'x' or self.turn_color == 'o':
            return True
        else:
            print('Only x or o! Please choose again: ')
            self.choose_player()
    
    def check_game_status(self):
        if self.count_tokens < self.width*self.height:
            self.game_status = 'active'
        else:
            self.game_status = 'over'
            print('Full board!') 

        for i in self.axis_strings(self.position[0],self.position[1]):
            if self.turn_color * self.win in i:
                self.game_status = 'over'
                self.won_by = self.turn_color 
                print(self.player(), '(', self.turn_color,')', ' winns!')

    def drop(self, color, slot):
        if self.turn_color == None:
                self.turn_color = color
        assert self.turn_color == color, 'Wrong Player'
        tile = Tile(color, slot, self.lines[slot])
        try:           
            self.board[tile.position[1]][tile.position[0]] = tile.color
            self.lines[slot] += 1
            self.position = tile.position[::-1]
            self.check_game_status()
            if self.game_status == 'active':
                self.count_tokens += 1
                if self.turn_color == 'x':
                    self.turn_color = 'o'
                else:
                    self.turn_color = 'x'
            return tile
        except IndexError:
            board.drop(board.turn_color, int(input('Out of range! Please, choose slot: ')) - 1)

    def player(self):
        if self.count_tokens % 2 == 0:
            return 'Player 1'
        else:
            return 'Player 2'

    @staticmethod
    def load(string): 
        board_width = 0
        board_height = 0
        load_board = []
        for i in string.splitlines()[::-1]:
            if len(i) > 0:
                load_board.append(list(i))
                board_height += 1
                board_width = len(i)    
        board = Board(board_width, board_height)
        board.board = load_board
        return board
    

    def axis_strings(self, x, y):
        self.position = (x, y)
        list_of_strings = []
        list_of_axis_strings = []
        check_count = 0
        check_position = [0, 0]
        for i in self.DIRECTIONS:   
            if check_count < 4:
                list_of_strings.append(self.board[self.position[0]][self.position[1]])
            else:
                list_of_strings.append('')
            check_position[0] = (self.position[0]+i[0])
            check_position[1] = (self.position[1]+i[1])
            for j in range(self.width-1):
                if check_position[0] >= 0 and check_position[1] >= 0 and check_position[1] < self.width and check_position[0] < self.height: 
                    list_of_strings[check_count] = list_of_strings[check_count] + (self.board[check_position[0]][check_position[1]])
                    check_position[0] = (check_position[0]+i[0])
                    check_position[1] = (check_position[1]+i[1])
            check_count += 1
        list_of_axis_strings.append(list_of_strings[4][::-1] + list_of_strings[0])
        list_of_axis_strings.append(list_of_strings[5][::-1] + list_of_strings[1])
        list_of_axis_strings.append(list_of_strings[6][::-1] + list_of_strings[2])
        list_of_axis_strings.append(list_of_strings[7][::-1] + list_of_strings[3])
        return list_of_axis_strings

class Tile:
    def __init__(self, color, x, y):
        self.color = color
        self.position = (x, y)



if __name__ == '__main__':
    '''
    def trim_board(ascii_board):
        return '\n'.join([i.strip() for i in ascii_board.splitlines()])
    t = trim_board
    board = Board.load(t("""
    o..
    o..
    xxx
    """))'''

   
   
    board = Board(5,5)

    print('Starting Game!')
    print()
    board.choose_player()

    while board.game_status == 'active':
        print(board.player())
        print(board.ascii())
        
        board.drop(board.turn_color, int(input('Please, choose slot: ')) - 1)
        
    
        

      
