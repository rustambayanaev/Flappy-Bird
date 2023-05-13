"""Задание для nFactorial
Автор Рустам Б.Б. дата создания 13.05.2023
"""
import pygame, sys, random

def draw_floor():
	# Отрисовка поверхности пола
	screen.blit(floor_surface, (floor_x_position, 900))
	screen.blit(floor_surface, (floor_x_position + 576, 900))
def update_score(score, high_score):
	# Обновление лучшего результата при достижении нового рекорда
	if score > high_score:
		high_score = score
	return high_score
def move_pipes(pipes):
    # Перемещение труб
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def rotate_bird(bird):
    # Поворот птицы в зависимости от движения
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird
def bird_animation():
    # Анимация птицы
    new_bird = bird_frames[bird_index]
    new_bird_rectangle = new_bird.get_rect(center=(100, bird_rectangle.centery))
    return new_bird, new_bird_rectangle
def draw_pipes(pipes):
	# Отрисовка труб
	for pipe in pipes:
		if pipe.bottom >= 1024:
			# Отрисовка нижней трубы
			screen.blit(pipe_surface, pipe)
		else:
			# Отрисовка перевернутой верхней трубы
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    # Проверка столкновения птицы с трубами
    for pipe in pipes:
        if bird_rectangle.colliderect(pipe):
            death_sound.play()
            return False

    # Проверка столкновения птицы с верхней и нижней границами экрана
    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 900:
        return False

    return True
def create_pipe():
	# Создание новых труб
	random_pipe_position = random.choice(pipe_height)
	# Нижняя труба
	bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_position))
	# Верхняя труба
	top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_position - 300))
	return bottom_pipe, top_pipe
def score_display(game_state):
    # Отображение счета на экране в зависимости от состояния игры
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rectangle)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rectangle = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rectangle)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rectangle = high_score_surface.get_rect(center=(288, 185))
        screen.blit(high_score_surface, high_score_rectangle)

# Инициализация Pygame
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('./assets/04B_19.TTF', 40)

# Переменные для игры
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Загрузка фоновой и поверхности пола
background_surface = pygame.image.load('assets/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

# Загрузка изображений птицы
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)  # Таймер для смены кадров птицы

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # Таймер для создания новых труб каждые 1.2 секунды
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rectangle = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rectangle.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rectangle = bird_animation()

    screen.blit(background_surface, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rectangle.centery += bird_movement
        screen.blit(rotated_bird, bird_rectangle)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rectangle)
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_x_position -= 1
    draw_floor()
    if floor_x_position <= -576:
        floor_x_position = 0

    pygame.display.update()
    clock.tick(120)



#Мой личный рекорд в этой игре 72)))