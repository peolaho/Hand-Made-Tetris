import time
import os
import random
import sys

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
BLOCK_CHAR = "1"

def get_front_row(row, column):
    if index_exists(next_blocks[row], column): 
        next_block_line = (' '.join(map(str, next_blocks[row][column])))
        text = ''
        for i in next_block_line.split():
            if i == '1':
                text += (COLOR + '  ' + RESET_COLOR)
            else:
                text += (RESET_COLOR + '  ' + RESET_COLOR)
        text_len = len((text.replace(COLOR, '').replace(RESET_COLOR, '')))
        
        front_spaces = (((RESET_COLOR + ' ' + RESET_COLOR) * (5)))
        backend_spaces = (((RESET_COLOR + ' ' + RESET_COLOR) * (14 - (5 + text_len))))
        return (RESET_COLOR + front_spaces + RESET_COLOR + text + RESET_COLOR + backend_spaces + RESET_COLOR)
    else:
        return (RESET_COLOR + '  ' * 7)

# 보드 초기화
def create_board():

    return [
        [0] * BOARD_WIDTH 
        for _ in range(BOARD_HEIGHT)
        ]

def move_cursor(x, y):
    print(f"\033[{y};{x}H", end="")
    
def index_exists(arr, i):
    return (0 <= i < len(arr)) or (-len(arr) <= i < 0)

# 보드 출력
def print_board(board, block=None, block_x=0, block_y=0):
    temp_board = [row[:] for row in board]  # 보드 복사

    # 현재 블록을 보드에 그리기
    if block:
        for y, row in enumerate(block):
            for x, cell in enumerate(row):
                if cell:
                    temp_board[block_y + y][block_x + x] = BLOCK_CHAR
    # 보드 출력
    screen = ''
    for i, row in enumerate(temp_board):
        screen += ' ' * ((terminal_column // 3) + (terminal_column // 37))
        match i:
            case 1:
                screen += ('Next --------;')
            case 2 : screen += get_front_row(0,0)
            case 3 : screen += get_front_row(1,1)
            case 5 : screen += get_front_row(1,0)
            case 6 : screen += get_front_row(1,1)
            case 8 : screen += get_front_row(2,0)
            case 9 : screen += get_front_row(2,1)
                
            case _:
                screen += ('  ' * 7)
        screen += (
            '\033[1;37m |' +
            ''.join(map(str, row))
              .replace('0', '  ')
              .replace(BLOCK_CHAR, (COLOR + '  ' + RESET_COLOR)) +
            '\033[1;37m| \033[0m'
            )
        match i:
            case 4:
                screen += (f'Line :{line}\n')
            case 7:
                screen += (f'Score:{score}\n')
            case 10:
                screen += (f'Level:{level}\n')
            case 13:
                screen += ('Hold -------;\n')
                holded_block = hold_block
                for i in range(4):
                    holded_block = [  
                    list(row) for row in 
                    zip(*holded_block[::-1])
                    ]
                    if len(holded_block) <= 2:
                        break
            case 14:
                if index_exists(holded_block, 0): 
                    screen += (''.join(map(str, holded_block[0])).replace('0', '  ').replace('1', (COLOR + '  ' + RESET_COLOR)) + '     \n')
                else:
                    screen += '\n'
            case 15:
                if index_exists(holded_block, 1): 
                    screen += (''.join(map(str, holded_block[1])).replace('0', '  ').replace('1', (COLOR + '  ' + RESET_COLOR)) + '     \n')
                else:
                    screen += '\n'
                
            case _:
                screen += ('\n')   
    
    move_cursor(1, 1)
    screen_height_half = len(screen.split('\n')) // 2 + 3
    for i in range(screen_height_half):
        print()
    
    print(screen)

    text = "\nControls: A - Left | D - Right | R - Rotate | S - Down | Q - Quit"
    spaces = (' ' * int(((terminal_column - len(text)) // 2)))
    
    print('\n' + spaces + text)
    
    text = str(next_blocks)
    try:
        print (''.join(map(str, next_blocks[0][0])))
        print (''.join(map(str, next_blocks[0][1])))
        print ()
        print (''.join(map(str, next_blocks[1][0])))
        print (''.join(map(str, next_blocks[1][1])))
        print ()
        print (''.join(map(str, next_blocks[2][0])))
        print (''.join(map(str, next_blocks[2][1])))
    except:
        pass

# 블록이 보드에 유효한지 검사
def is_valid_position(board, block, block_x, block_y):
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                # 보드 경계 확인
                if block_x + x < 0 or block_x + x >= BOARD_WIDTH or block_y + y >= BOARD_HEIGHT:
                    return False
                # 블록이 이미 있는 위치인지 확인
                if block_y + y >= 0 and board[block_y + y][block_x + x]:
                    return False
    return True


# 블록을 보드에 고정
def place_block(board, block, block_x, block_y):
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                board[block_y + y][block_x + x] = BLOCK_CHAR

# 가득 찬 라인 삭제
def clear_lines(board, block, block_x, block_y):
    anime_board = []
    new_board = []
    lines_cleared = 0
    for i, row in enumerate(board):
        if all(row):
            lines_cleared += 1
            anime_board.insert(i, [0] * BOARD_WIDTH)
            new_board.insert(0, [0] * BOARD_WIDTH)
        else:   
            new_board.insert(i, row)
            anime_board.insert(i, row)
    
    if not board == new_board:
        print_board(board,block, block_x, block_y)
        time.sleep(0.3)
        print_board(anime_board)
        time.sleep(0.7)
        print_board(board,block, block_x, block_y)
        time.sleep(0.7)
    return new_board, lines_cleared

# 블록 회전
def rotate_block(block):
    return [
        list(row) for row in 
            zip(*block[::-1])
    ] 

def get_center(current_block):
    return (BOARD_WIDTH // 2 - len(current_block[0]) // 2), 0

def get_random_tetris_block():
    return random.choice(TETROMINOS)

def set_block_release(next_blocks):
    current_block = next_blocks[0]
    next_blocks = [next_blocks[1], next_blocks[2], get_random_tetris_block()]
    return next_blocks, current_block

def start_game():
    os.system('clear')
    front_spaces = ' ' * ((terminal_column - 87) // 2)
    print('\n' * ((terminal_row + 9) // 3))
    print(front_spaces + ("##### ### ##### ###   #   ###").replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   #     #   #  #  #  #  ") .replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   #     #   #  #  #  #   ").replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   ###   #   ###   #   ##").replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   #     #   #  #  #     #") .replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   #     #   #  #  #     #") .replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print(front_spaces + ("  #   ###   #   #  #  #  ###") .replace(' ', '   ').replace('#', COLOR + '   ' + RESET_COLOR))
    print('\n\n')
    front_spaces = ' ' * ((terminal_column - 18) // 2)
    print(front_spaces + "Press to Continue"); _ = sys.stdin.read(1)
    return 0

def end_game(time_set):
    print(f":{COLORS[3]}  {RESET_COLOR}; You Game Over!")
    print(f":{COLORS[4]}  {RESET_COLOR}; You  Cleared  {line} Lines")
    print(f":{COLORS[5]}  {RESET_COLOR}; You  Got      {score} Scores")
    print(f":{COLORS[6]}  {RESET_COLOR}; Your Level Is {level} Levels")
    print('\n\n')
    print(f"{COLOR}| \033[1;37m YOU PLAYED {round(time_set[0] - time_set[1], 2)} SECONDS |{RESET_COLOR}")
    print("Press to Continue"); _ = sys.stdin.read(1)
    sys.exit()

def check_level(score):
    if   score <= 4800: return 0 ,16
    elif score <= 10800: return 1 ,14.3
    elif score <= 22800: return 2 ,12.6
    elif score <= 33600: return 3 ,11
    elif score <= 52800: return 4 ,9.3
    elif score <= 68400: return 5 ,7.7
    elif score <= 94800: return 6 ,6
    elif score <= 115200: return 7 ,4.3
    elif score <= 148800: return 8 ,2.7
    elif score <= 174000: return 9 ,2
    elif  score <= 214800: return 10,1.7
    elif  score <= 244800: return 11,1.7
    elif  score <= 292800: return 12,1.7
    elif  score <= 327600: return 13,1.3
    elif  score <= 382800: return 14,1.3
    elif  score <= 422400: return 15,1.3
    elif  score <= 484800: return 16,1
    elif  score <= 529200: return 17,1
    elif  score <= 598800: return 18,1
    elif  score <= 648000: return 19,0.66
    elif  score <= 724800: return 20,0.66
    elif  score <= 778800: return 21,0.66
    elif  score <= 862800: return 22,0.66
    elif  score <= 921600: return 23,0.66
    elif  score >= 999999: return 24,0.66
    elif  score >= 999999: return 25,0.66
    elif  score >= 999999: return 26,0.66
    elif  score >= 999999: return 27,0.66
    elif  score >= 999999: return 28,0.33

# 메인 게임 루프
def main():
    global next_blocks
    global score, line, level
    
    board = create_board()
    current_block = get_random_tetris_block()
    block_x, block_y = get_center(current_block)

    speed = 16  # 초기 속도
    start_time = time.time()
    last_time = time.time()
    
    next_blocks, current_block = set_block_release([get_random_tetris_block(), get_random_tetris_block(), get_random_tetris_block()])
    
    os.system('clear')
    timeout = 1 / FPS
    while True:
        print_board(board, current_block, block_x, block_y)

        # 시간에 따라 블록 하강
        if time.time() - last_time > speed / BOARD_HEIGHT:
            if is_valid_position(board, current_block, block_x, block_y + 1):
                block_y += 1
                score += 1
            else:
                os.system('clear')
                place_block(board, current_block, block_x, block_y)
                board, lines_cleared = clear_lines(board, current_block, block_x, block_y)
                score += lines_cleared * 100
                line += lines_cleared    
                level, speed = check_level(score)
                
                next_blocks, current_block = set_block_release(next_blocks)
                
                block_x, block_y = get_center(current_block)
                if not is_valid_position(board, current_block, block_x, block_y):
                    end_game([last_time, start_time])
            last_time = time.time()

        # 사용자 입력 처리
        if os.name == 'nt': pass # Windows
        else:  # Linux/Mac
            import tty, termios
            import select
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)  # 입력을 버퍼 없이 바로 받기
                rlist, _, _ = select.select([sys.stdin], [], [], timeout)
                if rlist: 
                    key = sys.stdin.read(1)
                    if key == 'a' and is_valid_position(board, current_block, block_x - 1, block_y):
                        block_x -= 1
                    elif key == 'd' and is_valid_position(board, current_block, block_x + 1, block_y):
                        block_x += 1
                    elif key == 'r':
                        rotated_block = rotate_block(current_block)
                        if is_valid_position(board, rotated_block, block_x, block_y):
                            current_block = rotated_block
                    elif key == 's' and is_valid_position(board, current_block, block_x, block_y + 1):
                        block_y += 1
                        score += 1
                    elif key == '\n':
                        for i in range(BOARD_HEIGHT):
                            if not is_valid_position(board, current_block, block_x, block_y + i):
                                block_y = (i - 1)
                                score += (i - 1)
                    elif key == 'c':
                        global hold_block
                        hold_block = get_random_tetris_block()
                        if not hold_block[0]:
                            if is_valid_position(board, hold_block, block_x, block_y):
                                temp_block = hold_block
                                hold_block = current_block
                                current_block = temp_block
                        else:
                            if is_valid_position(board, hold_block, block_x, block_y):
                                temp_block = current_block
                                current_block = hold_block
                                hold_block = temp_block
                    elif key == 'q':
                        end_game([last_time, start_time])
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            time.sleep(1 / FPS)

if __name__ == "__main__":
    start_game()
    main()
