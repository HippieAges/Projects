import pygame, sys, random, time
from pygame.locals import *
from TetrisConstants import *

def main():
    global DISPLAYSURF, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Tetris')

    DISPLAYSURF.fill(BLACK)

    # print(pygame.font.get_fonts())

    gameLoop()

def createBlankBoard():
    board = []
    for i in range(BOARDHEIGHT):
        board.append(["."]*BOARDWIDTH)
    return board

def addingPieceToBoard(board, completePiece):
    for x in range(PIECEWIDTH):
        for y in range(PIECEHEIGHT):
            if completePiece['rotation']['x']['y'] != '.':
                board[x + completePiece['x']][y + completePiece['y']] = 'X'

def movePlacedBlocksDown(board):
    currentRow = 0

    for i in range(BOARDWIDTH): # columns
        for j in range(1, BOARDHEIGHT): # rows
            currentRow = BOARDHEIGHT-j-1
            if(board[currentRow][i] == '.'):
                break
            elif(board[currentRow][i] == 'X'):
                if(board[currentRow+1][i] == '.'):
                    board[currentRow+1][i] = 'X'
                    board[currentRow][i] = '.'

    return board

def deleteLine(score, board):
    filledTiles = 0
    currentColumn = 0
    index = 0

    while index < BOARDWIDTH:
        currentColumn = BOARDWIDTH-index-1
        if(board[BOARDHEIGHT-1][currentColumn] == '.'):
            break
        elif(board[BOARDHEIGHT-1][currentColumn] == 'X'):
            filledTiles += 1
            board[BOARDHEIGHT-1][currentColumn] = '.'
            if(filledTiles == BOARDWIDTH):
                score += BOARDWIDTH
                index = 0 # start at the first column again
                filledTiles = 0
                board[:] = movePlacedBlocksDown(board)
                continue
        index += 1

    return score

def validTopPosition(board, piece):
    # if we try to place a piece right above the screen with something placed at the top y position, then Game Over
    if board[0][piece['x']] == 'X' and piece['y'] == -1:
        return False
    return True

def pieceOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y >= 0 and y < BOARDHEIGHT

def validBoardPosition(board, piece, adjX = 0, adjY = 0):
    if not validTopPosition(board, piece):
        return False
    print("Check len of board: " + str(len(board)))
    print("Check piecex & piecy: " + str(piece['x']) + "," + str(piece['y']))
    for y in range(PIECEWIDTH):
        for x in range(PIECEHEIGHT):
            # print(board[y + piece['y'] + adjY])
            if piece['y'] < 0:
                continue
            if not pieceOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjX):
                return False
            elif board[x + piece['x'] + adjX][y + piece['y'] + adjY] == 'X':
                return False
    return True

def movePiece(event):
    if event.key == K_a or event.key == K_LEFT:
        return LEFT
    elif event.key == K_d or event.key == K_RIGHT:
        return RIGHT
    elif event.key == K_s or event.key == K_DOWN:
        return DOWN
    return -1
        
# argument: rotationList - completePiece.get('piece')
#           index - current rotated piece
def rotatePiece(rotationList, index, event):
    if event.key == K_w or event.key == K_UP:
        if index + 1 < len(rotationList[index]):
            index += 1
            return index
        else:
            index = 0
            return index
    return -1

def obtainNewPiece():
    piece = random.choice(list(PIECES.keys()))

    completePiece = { 'color': COLOR.get(piece),
                      'x': int(BOARDWIDTH/2),
                      'y': -4, # make sure the I piece isn't visible when starting
                      'rotation': 0, # start at the default piece 
                      'piece': piece }
    return completePiece

def drawOutline():
    pygame.draw.rect(DISPLAYSURF, BLUE, (500,100,440,800), 5)

def pauseGame():
    DISPLAYSURF.fill(BLACK)
    display(100, "PAUSED")
    display(36, "Press any key(except P) to continue.", UNDERTITLE)

def scoreBoard(score):
    level = int(score/100) + 1
    fontObj = pygame.font.SysFont("comicsansms", 36)

    textSurfaceObj = fontObj.render("Score: %s" % score, True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (1200,100)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = fontObj.render("Level: %d" % level, True, WHITE)
    textRectObj.center = (1200,150)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = fontObj.render("Next:", True, WHITE)
    textRectObj.center = (1200,200)

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def display(sizeFont, msg, underTitle = 0):
    fontObj = pygame.font.SysFont("comicsansms", sizeFont)
    textSurfaceObj = fontObj.render(msg, True, WHITE)
    rect = textSurfaceObj.get_rect()
    rect.center = (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)+underTitle)
    DISPLAYSURF.blit(textSurfaceObj, rect)
    return rect

def displayTitle(title):

    titleRectObj = display(100, title)
    keyRectObj = display(36, "Please press a key to play.", UNDERTITLE)

    return [titleRectObj,keyRectObj]

def removeTitle(textRectObj):

    def removeDisplay(sizeFont, index):
        fontObj = pygame.font.SysFont("comicsansms", sizeFont)
        DISPLAYSURF.fill(BLACK,textRectObj[index])
        textSurfaceObj = fontObj.render("", True, BLACK)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj[0])

    removeDisplay(100, 0)
    removeDisplay(36, 1)

def gameLoop():

    score = 0
    fallingFreq = 0.26 # falling every 26th of a second in the beginning

    moveSidewaysTime = time.time()
    moveDownTime = time.time()
    fallTime = time.time()

    keyPressed = False
    moveLeftKey = False
    moveRightKey = False
    moveDownKey = False

    moveDirection = -1
    rotatedPiece = None
    currentIndex = 0
    priorIndex = 0
    rect = [(),()]

    board = createBlankBoard()

    currentPiece = obtainNewPiece()
    nextPiece = obtainNewPiece()

    while True: # main game loop

        if currentPiece == None:
            currentPiece = nextPiece
            nextPiece = obtainNewPiece()

            fallTime = time.time()

            if not validBoardPosition(board, currentPiece):
                return

        if not keyPressed:
            rect = displayTitle("TETRIS")

        for event in pygame.event.get([QUIT,KEYUP,KEYDOWN]):

            moveDirection = movePiece(event)
            priorIndex = currentIndex
            rotatedPiece = rotatePiece(currentPiece.get('piece'), currentIndex, event)

            if rotatedPiece != -1:
                currentIndex = rotatedPiece
                if not validBoardPosition(board, currentPiece):
                    currentIndex = priorIndex
                currentPiece['rotation'] = currentIndex

            if event.type == QUIT or event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                keyPressed = True
                removeTitle(rect)
                DISPLAYSURF.fill(BLACK)
                drawOutline()
                scoreBoard(score)

                if event.key == K_p:
                    pauseGame()
                    moveSidewaysTime = time.time()
                    moveDownTime = time.time()
                    fallTime = time.time()
                elif event.key == K_LEFT or event.key == K_a:
                    moveLeftKey = False
                elif event.key == K_RIGHT or event.key == K_d:
                    moveRightKey = False
                elif event.key == K_DOWN or event.key == K_w:
                    moveDownKey = False

            if movePiece(event) == LEFT and validBoardPosition(board, currentPiece, adjX = -1):
                currentPiece['x'] -= 1
                moveLeftKey = True
                moveRightKey = False
                moveSidewaysTime = time.time()
            elif movePiece(event) == RIGHT and validBoardPosition(board, currentPiece, adjX = 1):
                currentPiece['x'] += 1
                moveLeftKey = False
                moveRightKey = True
                moveSidewaysTime = time.time()
            elif movePiece(event) == DOWN and validBoardPosition(board, currentPiece, adjY = 1):
                currentPiece['y'] += 1
                moveDownKey = True
                moveDownTime = time.time()

        # to prevent the user from having to constantly click on a key #
        if (moveLeftKey or moveRightKey) and time.time() - moveSidewaysTime > MOVESIDEWAYSFREQ:
            if moveLeftKey and validBoardPosition(board, currentPiece, adjX = -1):
                currentPiece['x'] -= 1
            elif moveRightKey and validBoardPosition(board, currentPiece, adjX = 1):
                currentPiece['x'] += 1
            moveSidewaysTime = time.time()

        if moveDownKey and time.time() - moveDownKey > MOVEDOWNFREQ:
            if validBoardPosition(board, currentPiece, adjY = 1):
                currentPiece['y'] += 1
            moveDownTime = time.time()

        if keyPressed and time.time() - fallTime > fallingFreq:
            print("calling validBoardPosition in > falllingFreq")
            if not validBoardPosition(board, currentPiece, adjY = 1):
                addingPieceToBoard(board, currentPiece)
                score = deleteLine(score, board)
                fallingFreq = 0.27 - (int((score / 100)+1) * 0.01)
                currentPiece = None
            else:
                currentPiece['y'] += 1
                fallTime = time.time()
        # print(PIECES[nextPiece['piece']][nextPiece['rotation']][0][0])
        if keyPressed:
            drawBoardBoxes(board, currentPiece['color'])
            drawPiece(nextPiece, pixelx=1200, pixely=250)
            if currentPiece != None:
                drawPiece(currentPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBoardBoxes(board, color):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawIndividualBoxes(x, y, board[y][x], color)

def drawIndividualBoxes(x, y, board, color, pixelx = None, pixely = None):

            if pixelx == None and pixely == None:
                pixelx = XMARGIN + (x * PIECEWIDTH)
                pixely = YMARGIN + (y * PIECEHEIGHT)

            if board == 'X':
                pygame.draw.rect(DISPLAYSURF, color, (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))

def drawPiece(piece, pixelx = None, pixely = None):
    currentPiece = PIECES[piece['piece']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx = XMARGIN + (piece['x'] * BOXSIZE)
        pixely = YMARGIN + (piece['y'] * BOXSIZE)
    # print(piece)
    
    for x in range(PIECEWIDTH):
        for y in range(PIECEHEIGHT):
            drawIndividualBoxes(None, None, currentPiece[x][y], piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

main()