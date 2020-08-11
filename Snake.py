import pygame
from pygame.locals import *
from random import randint

WINDOWWIDTH = 1440
WINDOWHEIGHT = 900
SQWIDTH = SQHEIGHT = 40
SCOREBOARDX = int(WINDOWWIDTH/SQWIDTH)
SCOREBOARDY = int(WINDOWHEIGHT/SQHEIGHT)

FPS = 30
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (125,125,125)
GREEN = (0,255,0)
RED = (255,0,0)

def create_screen() -> None:
    global SURFACEDISPLAY
    pygame.init()
    SURFACEDISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Snake")

def game_loop():
    fpsClock = pygame.time.Clock()
    user_quits = False
    eaten = False
    direction = ''
    snake_pos = '-1'
    score = 0
    snake_parts = []

    x_coord = int(WINDOWWIDTH/2)-int(SQWIDTH/2)
    y_coord = int(WINDOWHEIGHT/2)-int(SQHEIGHT/2)
    food_x = randint(0, int(WINDOWWIDTH/SQWIDTH)-1)*SQWIDTH
    food_y = randint(0, int(WINDOWHEIGHT/SQHEIGHT)-1)*SQWIDTH

    while not user_quits:

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                user_quits = True

            direction = update_snake_direction(direction, event)
            
        if not hit_boundary(x_coord, y_coord) and not hit_self(snake_parts):
            
            SURFACEDISPLAY.fill(BLACK)
            score_board(score)
            drawn_snake, snake_parts = draw_snake(x_coord, y_coord, score, snake_pos, snake_parts)
            drawn_food = pygame.draw.rect(SURFACEDISPLAY, RED, (food_x, food_y, SQWIDTH, SQHEIGHT))

            x_coord, y_coord = update_snake_coordinates(direction, x_coord, y_coord)                

            if drawn_snake.colliderect(drawn_food):
                pygame.draw.rect(SURFACEDISPLAY, BLACK, (food_x, food_y, SQWIDTH, SQHEIGHT))
                eaten = True
                score += 1

                if y_coord > drawn_snake.y:
                    snake_pos = 'up'
                elif y_coord < drawn_snake.y:
                    snake_pos = 'down'
                elif x_coord > drawn_snake.x:
                    snake_pos = 'left'
                elif x_coord < drawn_snake.x:
                    snake_pos = 'right'
            else:
                snake_pos = ''

            if eaten:
                food_x = randint(0, int(WINDOWWIDTH/SQWIDTH)-1)*SQWIDTH
                food_y = randint(0, int(WINDOWHEIGHT/SQHEIGHT)-1)*SQWIDTH
                eaten = False
            
        else:
            bottomleft_text, dimensions = display_gameover()
            display_tryagain(bottomleft_text, dimensions)

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()
    quit()

def score_board(score : int) -> None:
    fontObj = pygame.font.SysFont('timesnewroman', 36)
    textSurfaceObj = fontObj.render(f'Score: {score}', True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = (SCOREBOARDX, SCOREBOARDY)

    SURFACEDISPLAY.blit(textSurfaceObj, textRectObj)

def hit_self(snake_parts : list) -> bool:
    for index in range(1, len(snake_parts)):
        if snake_parts[0].x == snake_parts[index].x and \
           snake_parts[0].y == snake_parts[index].y:
           return True
    return False

def hit_boundary(x_coord : int, y_coord : int) -> bool:
    if x_coord >= WINDOWWIDTH or x_coord <= 0:
        return True
    elif y_coord >= WINDOWHEIGHT or y_coord <= 0:
        return True
    return False

def display_gameover() -> tuple:
    SURFACEDISPLAY.fill(BLACK)
    fontObj = pygame.font.SysFont('timesnewroman', 72)
    textSurfaceObj = fontObj.render('GAME OVER', True, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT/2))

    SURFACEDISPLAY.blit(textSurfaceObj, textRectObj)

    return textRectObj.bottomleft, (textRectObj.width, textRectObj.height)

def display_tryagain(bottomleft_text : tuple, dimensions : tuple) -> None:
    
    rectObj = pygame.draw.rect(SURFACEDISPLAY, WHITE, (bottomleft_text[0]+int(dimensions[0]/4), bottomleft_text[1]+int(SQHEIGHT/2), int(dimensions[0]/2), int(dimensions[0]/2)))

    fontObj = pygame.font.SysFont('timesnewroman', 36)
    textSurfaceObj = fontObj.render('RESTART', True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = rectObj.center

    SURFACEDISPLAY.blit(textSurfaceObj, textRectObj)

    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
            if rectObj.bottomright[0] > mouse[0] > rectObj.topleft[0] and \
               rectObj.bottomright[1] > mouse[1] > rectObj.topleft[1]:
                game_loop()

def draw_snake(x_coord : int, y_coord : int, score : int, snake_pos: str, snake_parts : list) -> tuple:
    
    if score == 0 and snake_pos == '-1':
        snake_parts.append(pygame.draw.rect(SURFACEDISPLAY, GREEN, (x_coord, y_coord, SQWIDTH, SQHEIGHT)))
        return snake_parts[0], snake_parts

    low_bound = 1
    going_down = False
    going_up = False
    going_left = False
    going_right = False

    if score > 1 :
        low_bound = (score - 1) * 4

    if snake_parts[0].x > x_coord:
        going_left = True
    elif snake_parts[0].x < x_coord:
        going_right = True
    elif snake_parts[0].y > y_coord:
        going_down = True
    elif snake_parts[0].y < y_coord:
        going_up = True

    if snake_pos == 'up':
        snake_parts = [pygame.Rect(x_coord, y_coord-(5*index)-(index*SQHEIGHT), SQWIDTH, SQHEIGHT) for index in range(low_bound, (4*score))]
    elif snake_pos == 'down':
        snake_parts = [pygame.Rect(x_coord, y_coord+(5*index)+(index*SQHEIGHT), SQWIDTH, SQHEIGHT) for index in range(low_bound, (4*score))]
    elif snake_pos == 'right':
        snake_parts = [pygame.Rect(x_coord+(5*index)+(index*SQWIDTH), y_coord, SQWIDTH, SQHEIGHT) for index in range(low_bound, (4*score))]
    elif snake_pos == 'left':
        snake_parts = [pygame.Rect(x_coord-(5*index)-(index*SQWIDTH), y_coord, SQWIDTH, SQHEIGHT) for index in range(low_bound, (4*score))]
    # print(snake_parts)
    for index in range(len(snake_parts)-1, 0, -1):
        snake_parts[index] = snake_parts[index-1]
        if going_left:
            pygame.draw.rect(SURFACEDISPLAY, GREEN, (snake_parts[index].x+5, snake_parts[index].y, SQWIDTH, SQHEIGHT))
        elif going_right:
            pygame.draw.rect(SURFACEDISPLAY, GREEN, (snake_parts[index].x-5, snake_parts[index].y, SQWIDTH, SQHEIGHT))
        elif going_down:
            pygame.draw.rect(SURFACEDISPLAY, GREEN, (snake_parts[index].x, snake_parts[index].y+5, SQWIDTH, SQHEIGHT))
        elif going_up:
            pygame.draw.rect(SURFACEDISPLAY, GREEN, (snake_parts[index].x, snake_parts[index].y-5, SQWIDTH, SQHEIGHT))
        # elif snake_pos == '':
        #     pygame.draw.rect(SURFACEDISPLAY, GREEN, (snake_parts[index].x, snake_parts[index].y, SQWIDTH, SQHEIGHT))

    snake_parts.pop(0) # to remove the 1st element & get a new 1st element
    snake_parts.insert(0, pygame.draw.rect(SURFACEDISPLAY, GREEN, (x_coord, y_coord, SQWIDTH, SQHEIGHT)))
    # print(snake_parts)
    return snake_parts[0], snake_parts

def update_snake_direction(direction : str, event : pygame.event) -> str:
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        if event.key == K_w or event.key == K_UP:
            direction = 'UP'
        elif event.key == K_s or event.key == K_DOWN:
            direction = 'DOWN'
        elif event.key == K_a or event.key == K_LEFT:
            direction = 'LEFT'
        elif event.key == K_d or event.key == K_RIGHT:
            direction = 'RIGHT'
    return direction

def update_snake_coordinates(direction : str, coord_x : int, coord_y : int) -> tuple:
    if direction == 'UP':
        coord_y -= 4
    elif direction == 'DOWN':
        coord_y += 4
    elif direction == 'LEFT':
        coord_x -= 4
    elif direction == 'RIGHT':
        coord_x += 4
    return (coord_x, coord_y)

def main() -> None:
    create_screen()
    game_loop()

main()