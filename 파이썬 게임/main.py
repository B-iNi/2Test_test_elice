import pygame
import random

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 이미지 로드
background_img = pygame.image.load("background.jpg")
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")
pipe_img_top = pygame.transform.flip(pipe_img, False, True)

# 새 변수
bird_x, bird_y = 50, HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -8
flap_counter = 0

# 파이프 변수
pipe_width = 70
pipe_gap = 150
pipes = []
speed = 3
score = 0

# 배경 스크롤 변수
bg_x = 0
bg_speed = 2

def create_pipe():
    height = random.randint(100, 400)
    pipes.append([WIDTH, height])

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe_img_top, (pipe[0], pipe[1] - pipe_img_top.get_height()))
        screen.blit(pipe_img, (pipe[0], pipe[1] + pipe_gap))

def move_pipes():
    global score
    for pipe in pipes:
        pipe[0] -= speed
    if pipes and pipes[0][0] < -pipe_width:
        pipes.pop(0)
        score += 1

def check_collision():
    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT:
        return True
    for pipe in pipes:
        if (pipe[0] < bird_x < pipe[0] + pipe_width and
            (bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap)):
            return True
    return False

def draw_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def reset_game():
    global bird_y, pipes, bird_velocity, score, game_over, bg_x
    bird_y = HEIGHT // 2
    pipes.clear()
    bird_velocity = 0
    score = 0
    game_over = False
    bg_x = 0

running = True
game_over = False
while running:
    # 배경 이동
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0
    
    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + WIDTH, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength
            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        # 새 이동
        bird_velocity += gravity
        bird_y += bird_velocity
        flap_counter += 1
        bird_angle = -bird_velocity * 3
        rotated_bird = pygame.transform.rotate(bird_img, bird_angle)
        
        # 파이프 이동 및 생성
        move_pipes()
        if not pipes or pipes[-1][0] < WIDTH - 200:
            create_pipe()
        
        # 충돌 체크
        if check_collision():
            game_over = True
        
    # 새 & 파이프 그리기
    draw_pipes()
    screen.blit(rotated_bird, (bird_x - bird_radius, bird_y - bird_radius))
    draw_score()
    
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 130, HEIGHT // 2))
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
