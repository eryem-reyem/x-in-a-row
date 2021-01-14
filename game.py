from collections import defaultdict

class Board: 
    DIRECTIONS = ((1 ,0), (1, -1), (1, 1), (0, 1), (-1, 0), (-1, 1), (-1, -1), (0, -1))
    def __init__(self, width, height, win=3):
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
        self.positions_index = defaultdict(list)
        self.win_options = self.get_win_options()
        self.cpu = None

    def get_possible_wins(self, pos, direction):
        possible_wins = set()
        column, row = pos
        d_column, d_row = direction
        new_colmun, new_row = column+d_column*(self.win-1), row+d_row*(self.win-1)
        
        if new_colmun < 0 or new_colmun >= self.width or new_row < 0 or new_row >= self.height:
            return False
        for i in range(self.win):
            possible_wins.add((column+d_column*i, row+d_row*i))

        return possible_wins

    def get_win_options(self):
        counter = 0
        win_options = {}
        known_possitions = set()
        
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                for direction in self.DIRECTIONS:
                    positions = self.get_possible_wins((column, row), direction)
                    if not positions or positions in known_possitions:
                        continue
                    win_options[counter] = [0, 0] # player '0' / player 'x'
                    for position in positions:
                        self.positions_index[position].append(counter)
                    known_possitions.add(frozenset(positions))
                    counter += 1

        return win_options

    def set_token(self, pos, player):
        x, y = pos
        a_win = False
        self.board[y][x] = 'o' if player else 'x'
        for i in self.positions_index[pos]:
            self.win_options[i][player] += 1
            if self.win_options[i][player] == 4:
                a_win = True
        self.count_tokens += 1
        self.lines[x] += 1

        return a_win

    def delete_token(self, pos, player):
        x, y = pos
        self.board[y][x] = '.'
        for i in self.positions_index[pos]:
            self.win_options[i][player] -= 1 
        self.count_tokens -= 1
        self.lines[x] -= 1

    def rate(self):
        score = 0
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                for i in self.positions_index[(column, row)]:
                    player_2, player_1 = self.win_options[i]
                    if player_1 > 0 and player_2 > 0: 
                        continue
                    score += player_1*10
                    score -= player_2*10
        return score

    def list_of_moves(self):
        moves = []
        for column in range(self.width):
            if self.lines[column] >= self.height:
                continue
            row = self.lines[column]
            moves.append((column, row))
        return moves

    def computer(self, player):
        rated_moves = []
        for move in self.list_of_moves():
            win = self.set_token(move, player)
            score = self.minimax(5, -999999, 999999, player, win)
            self.delete_token(move, player)
            rated_moves.append((score, move))
        rated_moves.sort(reverse=player)
        score, best_move = rated_moves[0]
        print(rated_moves)
        print(best_move)
        win = self.drop(self.turn_color, best_move[0])
        return win

    def minimax(self, cutoffs, alpha, beta, player, win):   # alpha beta pruning
        if win:
            return 99999+cutoffs if player else -99999-cutoffs
        if cutoffs == 0 or self.count_tokens == (self.height*self.width):  # or spielfeld voll
            return self.rate()
        player = not player
        value = -999999 if player else 999999
        for move in self.list_of_moves():
            #print(move, cutoffs)
            win = self.set_token(move, player)
            score = self.minimax(cutoffs-1, alpha, beta, player, win)
            self.delete_token(move, player)
            if player:
                value = max(value, score)
                alpha = max(value, alpha)
            else:
                value = min(value, score)
                beta = min(value, beta)
            if alpha >= beta:
                break
        return value      

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
                #print(self.ascii())
                #print(self.player(), '(', self.turn_color,')', ' winns!')

    def drop(self, color, slot):
        if self.turn_color == None:
                self.turn_color = color
        assert self.turn_color == color, 'Wrong Player'
        tile = Tile(color, slot, self.lines[slot])
        if self.turn_color == 'o':
            player = True
        else:
            player = False
        try:      
            #print((slot, self.lines[slot]))   
            self.position = tile.position [::-1]  
            self.set_token((slot, self.lines[slot]), player)
            self.check_game_status() 
            if self.game_status == 'active': 
                if self.turn_color == 'x':
                    self.turn_color = 'o'
                else:
                    self.turn_color = 'x'
            
            return tile
        except IndexError:
            board.drop(board.turn_color, int(input('Out of range! Please, choose slot: ')) - 1)

    def player(self):
        if self.count_tokens % 2 == 1:
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
    board = Board(7,6,4)

    print('Starting Game!')
    print()

    a = input('1=cpu   |     2=alone:   ')
    print(a)
    if a == '1':
        board.cpu = 0

    board.choose_player()

    while board.game_status == 'active':

        print(board.player())
        print(board.ascii())
        
        if board.cpu == 0 or board.cpu == None:
            board.drop(board.turn_color, int(input('Please, choose slot: ')) - 1)
            try:
                board.cpu += 1
            except:
                continue
        elif board.cpu == 1:
            if board.turn_color == 'o':
                player = True
            else:
                player = False
            board.computer(player)
            board.cpu -= 1

        
        
    
        

      
