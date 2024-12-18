import time
import os
import random
import sys

# 보드와 블록 설정
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 블록 모양 (테트로미노)
TETROMINOS = [
    [[1, 1, 1, 1]],                      # I 블록
    [[1, 1, 0], [0, 1, 1]],             # Z 블록
    [[0, 1, 1], [1, 1, 0]],             # S 블록
    [[1, 0, 0], [1, 1, 1]],             # J 블록
    [[0, 0, 1], [1, 1, 1]],             # L 블록
    [[1, 1], [1, 1]],                   # O 블록
    [[0, 1, 0], [1, 1, 1]]              # T 블록
]

# 블록 색상(숫자로 표현)
BLOCK_CHAR = "#"

# 보드 초기화
def create_board():
    return [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

# 보드 출력
def print_board(board, block=None, block_x=0, block_y=0):
    os.system('cls' if os.name == 'nt' else 'clear')  # 화면 지우기
    temp_board = [row[:] for row in board]  # 보드 복사

    # 현재 블록을 보드에 그리기
    if block:
        for y, row in enumerate(block):
            for x, cell in enumerate(row):
                if cell:
                    temp_board[block_y + y][block_x + x] = BLOCK_CHAR

    # 보드 출력
    for row in temp_board:
        print("".join(str(cell) if cell else "." for cell in row))
    print("\nControls: A - Left | D - Right | W - Rotate | S - Down | Q - Quit")

# 블록이 보드에 유효한지 검사
def is_valid_position(board, block, block_x, block_y):
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                if (block_x + x < 0 or block_x + x >= BOARD_WIDTH or 
                    block_y + y >= BOARD_HEIGHT or board[block_y + y][block_x + x]):
                    return False
    return True

# 블록을 보드에 고정
def place_block(board, block, block_x, block_y):
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                board[block_y + y][block_x + x] = BLOCK_CHAR

# 가득 찬 라인 삭제
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * BOARD_WIDTH)
    return new_board, lines_cleared

# 블록 회전
def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]

# 메인 게임 루프
def main():
    board = create_board()
    current_block = random.choice(TETROMINOS)
    block_x, block_y = BOARD_WIDTH // 2 - len(current_block[0]) // 2, 0

    score = 0
    speed = 0.5  # 초기 속도
    last_time = time.time()

    while True:
        print_board(board, current_block, block_x, block_y)

        # 시간에 따라 블록 하강
        if time.time() - last_time > speed:
            if is_valid_position(board, current_block, block_x, block_y + 1):
                block_y += 1
            else:
                place_block(board, current_block, block_x, block_y)
                board, lines_cleared = clear_lines(board)
                score += lines_cleared
                current_block = random.choice(TETROMINOS)
                block_x, block_y = BOARD_WIDTH // 2 - len(current_block[0]) // 2, 0
                if not is_valid_position(board, current_block, block_x, block_y):
                    print_board(board)
                    print("Game Over! Your Score:", score)
                    sys.exit()
            last_time = time.time()

        # 사용자 입력 처리
        if os.name == 'nt':  # Windows
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == 'a' and is_valid_position(board, current_block, block_x - 1, block_y):
                    block_x -= 1
                elif key == 'd' and is_valid_position(board, current_block, block_x + 1, block_y):
                    block_x += 1
                elif key == 'w':
                    rotated_block = rotate_block(current_block)
                    if is_valid_position(board, rotated_block, block_x, block_y):
                        current_block = rotated_block
                elif key == 's' and is_valid_position(board, current_block, block_x, block_y + 1):
                    block_y += 1
                elif key == 'q':
                    print("Game Quit! Your Score:", score)
                    sys.exit()
        else:  # Unix/Linux/Mac
            import tty, termios
            import select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    key = sys.stdin.read(1).lower()
                    if key == 'a' and is_valid_position(board, current_block, block_x - 1, block_y):
                        block_x -= 1
                    elif key == 'd' and is_valid_position(board, current_block, block_x + 1, block_y):
                        block_x += 1
                    elif key == 'w':
                        rotated_block = rotate_block(current_block)
                        if is_valid_position(board, rotated_block, block_x, block_y):
                            current_block = rotated_block
                    elif key == 's' and is_valid_position(board, current_block, block_x, block_y + 1):
                        block_y += 1
                    elif key == 'q':
                        print("Game Quit! Your Score:", score)
                        sys.exit()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()
