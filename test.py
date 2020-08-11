board = []
smolBoard = ['X','.','.','X','.','.','X','X','X','.']
for i in range(1,21):
    if(i == 16 or i == 17):
        board.append(smolBoard)
    elif(i == 18 or i == 19 or i == 20):
        board.append(["X"]*10)
    else:
        board.append(["."]*10)
# print(str(board))

def movePlacedBlocksDown(board):
    currentRow = 0

    for i in range(10): # column
        for j in range(1, 20): # row
            currentRow = 20-j-1
            if(board[currentRow][i] == '.'):
                break
            elif(board[currentRow][i] == 'X'):
                if(board[currentRow+1][i] == '.'):
                    board[currentRow+1][i] = 'X'
                    board[currentRow][i] = '.'

    return(board)

def deleteLine(score, board):
    filledTiles = 0
    currentColumn = 0
    i = 0
    while i < 10:
        currentColumn = 10-i-1
        # print(board[20-1][currentColumn])
        if(board[20-1][currentColumn] == '.'):
            break
        elif(board[20-1][currentColumn] == 'X'):
            filledTiles += 1
            board[20-1][currentColumn] = '.'
            # print(str(filledTiles))
            if(filledTiles == 10):
                # print("In here")
                i = 0 # start at the first column again
                filledTiles = 0
                board[:] = movePlacedBlocksDown(board)
                continue
        i += 1
    return(board)

# deleteLine(0, board)
print(str(deleteLine(0, board)))