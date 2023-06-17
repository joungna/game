import pygame
import random

pygame.init()

# 게임 창 크기 설정
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 480
BLOCK_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_TOP = WINDOW_HEIGHT - BOARD_HEIGHT * BLOCK_SIZE

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 128, 0)

# 게임 보드 초기화
board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

# Pygame 창 설정
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

# 블록 모양 설정
tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[2, 2, 0], [0, 2, 2]],  # Z
    [[0, 3, 3], [3, 3, 0]],  # S
    [[4, 0, 0], [4, 4, 4]],  # J
    [[0, 0, 5], [5, 5, 5]],  # L
    [[0, 6, 6], [6, 6, 0]],  # T
    [[7, 7], [7, 7]]  # O
]

# 블록 클래스 정의
class Tetrominoes:
    def __init__(self, shape):
        self.color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE])
        self.shape = shape
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape))] for x in range(len(self.shape[0])-1, -1, -1)]
    
    def move_left(self):
        self.x -= 1
        if self.is_colliding():
            self.x += 1
    
    def move_right(self):
        self.x += 1
        if self.is_colliding():
            self.x -= 1
    
    def move_down(self):
        self.y += 1
        if self.is_colliding():
            self.y -= 1
            self.freeze()
    
    def is_colliding(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if self.shape[y][x] != 0 and (self.y + y >= BOARD_HEIGHT or self.x + x < 0 or self.x + x >= BOARD_WIDTH or board[self.y + y][self.x + x] != 0):
                    return True
        return False
    
    def freeze(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if self.shape[y][x] != 0:
                    board[self.y + y][self.x + x] = self.color
    
    def draw(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[0])):
                if self.shape[y][x] != 0:
                    pygame.draw.rect(screen, self.color, (self.x*BLOCK_SIZE, BOARD_TOP + self.y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# 새로운 블록 생성 함수
def new_tetromino():
    return Tetrominoes(random.choice(tetrominoes))

# 줄이 꽉 찼는지 확인하고 제거하는 함수
def remove_full_lines():
    lines_removed = 0
    for y in range(BOARD_HEIGHT):
        if all(board[y]):
            del board[y]
            board.insert(0, [0] * BOARD_WIDTH)
            lines_removed += 1
    return lines_removed

# 게임 루프
def run_game():
    clock = pygame.time.Clock()
    current_tetromino = new_tetromino()
    next_tetromino = new_tetromino()
    score = 0
    game_over = False
    
    while not game_over:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.move_left()
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.move_right()
                elif event.key == pygame.K_DOWN:
                    current_tetromino.move_down()
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
        
        # 게임 로직 처리
        current_tetromino.move_down()
        if current_tetromino.is_colliding():
            current_tetromino.freeze()
            lines_removed = remove_full_lines()
            score += lines_removed ** 2
            current_tetromino = next_tetromino
            next_tetromino = new_tetromino()
            if current_tetromino.is_colliding():
                game_over = True
        
        # 화면 그리기
        screen.fill(BLACK)
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if board[y][x] != 0:
                    pygame.draw.rect(screen, board[y][x], (x*BLOCK_SIZE, BOARD_TOP + y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        current_tetromino.draw()
        next_tetromino.draw()
        pygame.display.update()
        
        # 게임 속도 설정
        clock.tick(10)
    
    pygame.quit()

# 게임 실행
run_game()