import os, random

terminal_column = os.get_terminal_size()[0]
terminal_row = os.get_terminal_size()[1]

score = 0
line =0
level =0
# 보드와 블록 설
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

FPS = 30

# 블록 모양 (테트로미노)
TETROMINOS = [
    [[1, 1, 1, 1]],                       # I 블록
    [[1, 1, 0], [0, 1, 1]],             # Z 블록
    [[0, 1, 1], [1, 1, 0]],             # S 블록
    [[1, 0, 0], [1, 1, 1]],             # J 블록
    [[0, 0, 1], [1, 1, 1]],             # L 블록
    [[1, 1], [1, 1]],                   # O 블록
    [[0, 1, 0], [1, 1, 1]]              # T 블록
]
COLOR = random.choice([
        '\033[47m',
        '\033[46m',
        '\033[45m',
        '\033[44m',
        '\033[43m',
        '\033[42m'
        '\033[41m',
])
 

COLORS = [
        '\033[47m',
        '\033[46m',
        '\033[45m',
        '\033[44m',
        '\033[43m',
        '\033[42m',
        '\033[41m'
        ]

RESET_COLOR = '\033[0m'

hold_block = []
next_blocks = []

# 블록 색상(숫자로 표현)
BLOCK_CHAR = "#"


