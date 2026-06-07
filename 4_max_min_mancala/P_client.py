# client to Mancala server. Lab4, DVA340, MDU.
# For students: you only need to fill out function decide_move(boardIn, playerTurnIn)
# it currently selects a random available move.
# To test your client: start Mancala_server.pyc, then your program and one bot in that order (server first, then clients)

# python Mancala.server.pyc

import socket
import time
from datetime import date
from multiprocessing.pool import ThreadPool


def decide_move(board_in, player_turn_in):
    #CHANGE THIS FILE TO CODE INTELLIGENCE IN YOUR CLIENT.
    # PLAYERMOVE IS '1'..'6'
    # BOARDIN CONSISTS OF 14 INTS. BOARDIN[0-5] ARE P1 HOLES, BOARDIN[6] IS P1 STORE
    # BOARDIN[7-12] ARE P2 HOLES, BOARDIN[13] IS P2 STORE
    best_val = -999
    best_move = '1'
    MAX_DEPTH = 3

    valid_moves = [m for m in range(1, 7) if correctPlay(m, board_in, player_turn_in)]

    for m in valid_moves:
        board_copy = board_in.copy()

        new_board, next_turn = play(player_turn_in, m, board_copy)

        move_val = minimax(new_board, MAX_DEPTH - 1, next_turn, player_turn_in, -999, 999)

        if move_val > best_val:
            best_val = move_val
            best_move = str(m)

    return best_move, "minimax_bot"


def is_game_over(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0


def evaluate(board, maximizing_player):
    print(maximizing_player)
    if maximizing_player == 1:
        my_store = board[6]
        opp_store = board[13]
    else:
        my_store = board[13]
        opp_store = board[6]
    return my_store - opp_store


def minimax(board: list[int], depth: int, current_turn: int, maximizing_player: int, alpha: float, beta: float) -> float:
    if depth == 0 or is_game_over(board):
        return evaluate(board, maximizing_player)

    valid_moves = [m for m in range(1, 7) if correctPlay(m, board, current_turn)]

    if not valid_moves:
        return evaluate(board, maximizing_player)

    if current_turn == maximizing_player:
        return minimax_me(board, depth, current_turn, maximizing_player, alpha, beta, valid_moves)
    else:
        return minimax_other(board, depth, current_turn, maximizing_player, alpha, beta, valid_moves)

def minimax_me(board: list[int], depth: int, current_turn: int, maximizing_player: int,
               alpha: float, beta: float, valid_moves: list[int]) -> float:

    best_score = -999

    for move in valid_moves:
        board_copy = board.copy()
        new_board, next_turn = play(current_turn, move, board_copy)

        score = minimax(new_board, depth - 1, next_turn, maximizing_player, alpha, beta)

        best_score = max(best_score, score)
        alpha = max(alpha, score)

        if beta <= alpha:
            break

    return best_score


def minimax_other(board: list[int], depth: int, current_turn: int, maximizing_player: int,
                  alpha: float, beta: float, valid_moves) -> float:

    best_score = 999

    for move in valid_moves:
        board_copy = board.copy()
        new_board, next_turn = play(current_turn, move, board_copy)

        score = minimax(new_board, depth - 1, next_turn, maximizing_player, alpha, beta)

        best_score = min(best_score, score)
        beta = min(beta, score)

        if beta <= alpha:
            break

    return best_score

def play(playerTurn: int, playerMove: int, boardGame):  
    #playerTurn ar 1 eller 2
    #playerMove ar 1..6
    #boardGame ar en 1x14 vektor
    if not correctPlay(playerMove, boardGame, playerTurn):
        print("Illegal move! break")
        return
    
    # Determine starting index based on playerTurn and playerMove
    idx = playerMove -1 + (playerTurn-1)*7 #-1 for p1, +6 for p2
    # grab stones from hole
    numStones:int  = boardGame[idx]
    boardGame[idx] = 0
    hand:int = numStones
    while hand > 0:
        #idx next hole
        idx = (idx +1) % 14 
        # Skip opponent's store
        if idx == 13 - 7*(playerTurn-1): #13 for p1, 6 for p2
            continue
        # add stone in hole, 
        boardGame[idx] += 1
        hand -= 1
    
    # end in store? get another turn. otherwise other players turn
    nextTurn = 3 - playerTurn
    if idx == 6 + 7*(playerTurn-1):
        nextTurn = playerTurn
    
    #end on own empty hole? score stone and opposite hole
    if boardGame[idx] == 1 and idx in range((playerTurn-1)*7,6+(playerTurn-1)*7):
        boardGame[idx] -= 1 #score stone in last hole
        boardGame[6+(playerTurn-1)*7] += 1 #and remove it from the hole
        boardGame[6+(playerTurn-1)*7] += boardGame[12 - idx] #also score stones from opposite hole
        boardGame[12 - idx] = 0 #and remove them from the hole
    return boardGame, nextTurn


def correctPlay(playerMove:int, board, playerTurn):
    correct = 0
    if playerMove in range(1,7) and board[playerMove-1 + (playerTurn-1)*7] > 0:
        correct = 1
    return correct


def countScorePlayer1(boardGame):
    (p1s, p2s) = countPoints(boardGame)
    return int(p1s - p2s)
    

def countPoints(boardGame):
    return (boardGame[6], boardGame[13])



def receive(socket):
    msg = ''.encode()

    try:
        data = socket.recv(1024)
        msg += data
    except:
        pass

    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())

    

# LET THE MAIN BEGIN



startTime = date(2020, 11, 9)
playerName = 'Nicolas_Beyers'
host = '127.0.0.1'
port = 30000
s = socket.socket()
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 20
print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')
while not gameEnd:
    asyncRetult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        time.sleep(0.01)
        if asyncRetult.ready():
            data = asyncRetult.get()
            received = 1
        currentTime = time.time() - startTime
    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1
    if data == 'N':
        send(s, playerName)
    if data == 'E':
        gameEnd = 1
    if len(data) > 1:
        board = [            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0,            0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2
        (move, bot_name) = decide_move(board, playerTurn)
    #    print('sending ', move)
        send(s, move)

        
#wait = input('Press ENTER to close the program.')
