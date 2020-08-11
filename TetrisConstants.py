FPS = 30
WINDOWWIDTH = 1440
WINDOWHEIGHT = 900
PIECEWIDTH = 5
PIECEHEIGHT = 5
BOARDWIDTH = 10
BOARDHEIGHT = 20
BOXSIZE = 20

MOVEDOWNFREQ = 0.1
MOVESIDEWAYSFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE)/2)
YMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 10 

LEFT = 0
RIGHT = 1
DOWN = 2

UNDERTITLE = 100

BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
CYAN = (0,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
ORANGE = (255,165,0)
PINK = (255,192,203)
PURPLE = (128,0,128)

SBLOCK = [[
    ".....",
    ".....",
    "..XX.",
    ".XX..",
    ".....",
],
[
    ".....",
    ".X...",
    ".XX..",
    "..X..",
    ".....",
]]

IBLOCK = [[
    "..X..",
    "..X..",
    "..X..",
    "..X..",
    ".....",
],
[
    ".....",
    ".....",
    "XXXX.",
    ".....",
    ".....",
]]

OBLOCK = [[
    ".....",
    ".....",
    ".XX..",
    ".XX..",
    ".....",
]]

ZBLOCK = [[
    ".....",
    ".....",
    ".XX..",
    "..XX.",
    ".....",
],
[
    ".....",
    "...X.",
    "..XX.",
    "..X..",
    ".....",
]]

TBLOCK = [[
    ".....",
    ".....",
    "..X..",
    ".XXX.",
    ".....",
],
[
    ".....",
    "..X..",
    "..XX.",
    "..X..",
    ".....",
],
[
    ".....",
    ".....",
    ".XXX.",
    "..X..",
    ".....",
],
[
    ".....",
    "..X..",
    ".XX..",
    "..X..",
    ".....",
]]

JBLOCK = [[
    ".....",
    "X....",
    "XXX..",
    ".....",
    ".....",
],
[
    "..XX.",
    "..X..",
    "..X..",
    ".....",
    ".....",
],
[
    ".....",
    ".....",
    "..XXX",
    "....X",
    ".....",
],
[
    ".....",
    ".....",
    "..X..",
    "..X..",
    ".XX..",
]]

LBLOCK = [[
    ".....",
    "....X",
    "..XXX",
    ".....",
    ".....",
],
[
    ".XX..",
    "..X..",
    "..X..",
    ".....",
    ".....",
],
[
    ".....",
    ".....",
    "XXX..",
    "X....",
    ".....",
],
[
    ".....",
    ".....",
    "..X..",
    "..X..",
    "..XX.",
]]

PIECES = {
    'O': OBLOCK,
    'L': LBLOCK,
    'J': JBLOCK,
    'I': IBLOCK,
    'Z': ZBLOCK,
    'T': TBLOCK,
    'S': SBLOCK
}

COLOR = {
    'O': YELLOW,
    'I': CYAN,
    'S': RED,
    'Z': GREEN,
    'L': ORANGE,
    'J': PINK,
    'T': PURPLE
}