import uuid
from flask import Flask, url_for, request, render_template, session
import game

#export FLASK_ENV=development

 
app = Flask(__name__)

app.secret_key = b'yuCie4naengaiquoimio'

all_boards = {}

@app.route("/")
def index():
    if not 'user_id' in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('game_index.html',  instruction='Play x in a row? Please ENTER!')

@app.route("/game_start/<string:name>", methods=['POST'])
def game_start(name):
    board = all_boards[session['user_id']] = game.Board(7,6,4)
    board.turn_color = 'x'
    if name == '1':
        board.cpu = 0
    print(board.cpu)
    return render_template('game_start.html', headline=board.player(), instruction='Please enter row!', 
    width=board.width, height=board.height, board=board.board[::-1], game_status=board.game_status)  

@app.route("/game_player2", methods=['POST', 'GET'])
def game_player2():
    board = all_boards[session['user_id']]
    if board.cpu == 0 or board.cpu == None:
        ainput = request.form['name']
        if int(ainput) <= board.width and board.lines[int(ainput)-1] < board.height:
            board.drop(board.turn_color, int(ainput)-1)
        try:
            board.cpu += 1
        except:
            pass
    elif board.cpu == 1:
        if board.turn_color == 'o':
            player = True
        else:
            player = False
        board.computer(player)
        board.cpu -= 1
    return render_template('game_player2.html',  headline=board.player(), instruction='Please enter row!',
     width=board.width, height=board.height, board=board.board[::-1], game_status=board.game_status, cpu=board.cpu) 

        
@app.route("/game_player1", methods=['POST'])
def game_player1():
    board = all_boards[session['user_id']]
    if board.cpu == 0 or board.cpu == None:
        ainput = request.form['name']
        if int(ainput) <= board.width and board.lines[int(ainput)-1] < board.height:
            board.drop(board.turn_color, int(ainput)-1)
        try:
            board.cpu += 1
        except:
            pass
    elif board.cpu == 1:
        if board.turn_color == 'o':
            player = True
        else:
            player = False
        board.computer(player)
        board.cpu -= 1
    return render_template('game_start.html', headline=board.player(), instruction='Please enter row!',
    width=board.width, height=board.height, board=board.board[::-1], game_status=board.game_status, cpu=board.cpu) 

@app.route("/win")
def win():
    board = all_boards[session['user_id']]
    return render_template('win.html', headline=board.player())


if __name__ == "__main__":
    app.run(port=5000, debug=True)
