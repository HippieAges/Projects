from __future__ import annotations
import pygame
from pygame.locals import *
from random import randint

class Apple:

    apple_color = (255,8,0) # apple candy red
    clear_color = (0,0,0) # black

    def __init__(self : Apple, window_frame : tuple, square_frame : tuple, sidebar_width : int):
        self.x_food = randint(0, int((window_frame[0]-sidebar_width)/square_frame[0])-1)*square_frame[0]
        self.y_food = randint(0, int(window_frame[1]/square_frame[1])-1)*square_frame[1]

    def draw_food(self : Apple, surface_display : pygame.Surface, square_frame : tuple) -> pygame.Rect:
        return pygame.draw.rect(surface_display, self.apple_color, (self.x_food, self.y_food, square_frame[0], square_frame[1]))

    def clear_drawn_food(self : Apple, surface_display : pygame.Surface, square_frame : tuple) -> None:
        pygame.draw.rect(surface_display, self.clear_color, (self.x_food, self.y_food, square_frame[0], square_frame[1]))    

    def update_apple_coord(self : Apple, surface_display : pygame.Surface, window_frame : tuple, square_frame : tuple, sidebar_width : int) -> pygame.Rect:
        self.x_food = randint(0, int((window_frame[0]-sidebar_width)/square_frame[0])-1)*square_frame[0]
        self.y_food = randint(0, int(window_frame[1]/square_frame[1])-1)*square_frame[1]

        return pygame.Rect(self.x_food, self.y_food, square_frame[0], square_frame[1])

class Snake:
    
    snake_color = (0,125,0) # dark green
    speed = 4
    num_parts = 1

    going_up = False
    going_down = False
    going_left = False
    going_right = False

    def __init__(self : Snake, window_frame : tuple, square_frame : tuple, sidebar_width : int) -> None:
        self.x_coord = int((window_frame[0]-sidebar_width)/2)-int(square_frame[0]/2)
        self.y_coord = int(window_frame[1]/2)-int(square_frame[1]/2)
        self.direction = 'none'
        self.snake_parts = {self.num_parts : [pygame.Rect(self.x_coord, self.y_coord, square_frame[0], square_frame[1]), self.direction]}

    def add_tail(self : Snake, square_frame : tuple, score : int) -> None:
        
        new_snake_parts = {}
        # print('In add_tail: ' + self.snake_parts[len(self.snake_parts)][1])

        # adds to the tail of the snake
        if self.snake_parts[len(self.snake_parts)][1] == 'up':
            new_snake_parts = {self.num_parts+count: 
            [pygame.Rect(self.x_coord, self.y_coord, 
            square_frame[0], square_frame[1]), self.direction] for count, _ in enumerate(range(self.num_parts, score*self.speed), start=1)}
        
        elif self.snake_parts[len(self.snake_parts)][1] == 'down':
            new_snake_parts = {self.num_parts+count: 
            [pygame.Rect(self.x_coord, self.y_coord, 
            square_frame[0], square_frame[1]), self.direction] for count, _ in enumerate(range(self.num_parts, score*self.speed), start=1)}                

        elif self.snake_parts[len(self.snake_parts)][1] == 'left':
            new_snake_parts = {self.num_parts+count: 
            [pygame.Rect(self.x_coord, self.y_coord, 
            square_frame[0], square_frame[1]), self.direction] for count, _ in enumerate(range(self.num_parts, score*self.speed), start=1)}

        elif self.snake_parts[len(self.snake_parts)][1] == 'right':
            new_snake_parts = {self.num_parts+count: 
            [pygame.Rect(self.x_coord, self.y_coord, 
            square_frame[0], square_frame[1]), self.direction] for count, _ in enumerate(range(self.num_parts, score*self.speed), start=1)}                
        
            # join the existing body with the new snake parts
        self.snake_parts = {**self.snake_parts, **new_snake_parts}

    def draw_snake(self : Snake, surface_display : pygame.Surface, square_frame : tuple, score : int, collided : bool = False) -> pygame.Rect:

        # step 1 - remove old head, add new head, and draw the head
        self.snake_parts.pop(1)
        self.snake_parts[1] = [pygame.Rect(self.x_coord, self.y_coord, square_frame[0], square_frame[1]), self.direction] 
        pygame.draw.rect(surface_display, self.snake_color, self.snake_parts[1][0])

        # step 2 - add the tail once an apple is consumed
        if collided:
            self.add_tail(square_frame, score)

        if score > 0:

            # for key in range(2, len(self.snake_parts)+1):

            #     prior_direction = self.snake_parts[key-1][1]
            #     current_direction = self.snake_parts[key][1]
            #     x_val = self.snake_parts[key-1][0].x
            #     y_val = self.snake_parts[key-1][0].y

            #     if prior_direction == 'up':
            #         self.snake_parts[key] = [pygame.Rect(x_val, y_val+square_frame[1]+5, square_frame[0], square_frame[1]), current_direction]
            #     elif prior_direction == 'down':
            #         self.snake_parts[key] = [pygame.Rect(x_val, y_val-square_frame[1]-5, square_frame[0], square_frame[1]), current_direction]
            #     elif prior_direction == 'left':
            #         self.snake_parts[key] = [pygame.Rect(x_val+square_frame[0]+5, y_val, square_frame[0], square_frame[1]), current_direction]
            #     elif prior_direction == 'right':
            #         self.snake_parts[key] = [pygame.Rect(x_val-square_frame[0]-5, y_val, square_frame[0], square_frame[1]), current_direction]

            # for key in range(len(self.snake_parts), 1, -1):
            #     self.snake_parts[key][1] = self.snake_parts[key-1][1]

            # step 3 - update the old positions to those of new ones
            for key in range(len(self.snake_parts), 1, -1):
                self.snake_parts[key] = self.snake_parts[key-1]

            # step 4 - draw the body of the snake
            for count, _ in enumerate(range(len(self.snake_parts)-1), start=2):
                pygame.draw.rect(surface_display, self.snake_color, self.snake_parts[count][0])
        
        return self.snake_parts[1][0]

    def update_snake_coord(self: Snake) -> None:
        keys = pygame.key.get_pressed()
        
        for _ in keys:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.going_up = True
                self.direction = 'up'
                self.going_down = self.going_left = self.going_right = False

            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.going_down = True
                self.direction = 'down'
                self.going_up = self.going_left = self.going_right = False

            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.going_left = True
                self.direction = 'left'
                self.going_up = self.going_down = self.going_right = False

            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.going_right = True
                self.direction = 'right'
                self.going_up = self.going_down = self.going_left = False

        if self.going_up: self.y_coord -= self.speed
        elif self.going_down: self.y_coord += self.speed
        elif self.going_left: self.x_coord -= self.speed
        elif self.going_right: self.x_coord += self.speed

    def hit_boundary(self : Snake, window_frame : tuple, square_frame : tuple, sidebar_width : int) -> bool:
        if self.x_coord <= 0 or self.x_coord >= window_frame[0] - square_frame[0] - sidebar_width:
            return True
        elif self.y_coord <= 0 or self.y_coord >= window_frame[1] - square_frame[1]:
            return True
        return False

    def hit_self(self : Snake) -> bool: # uncomment end of line 309 once Snake is working the way I want it with proper spacing between snake parts
        for key in self.snake_parts:

            if key != 1: # to exclude comparing the head against the head
                if self.snake_parts[key][0].colliderect(self.snake_parts[1][0]):
                    return True
        return False

class Applet:
    
    fps = 30
    score = 0
    sidebar_color = (255,229,180) # peach
    sidebar_sep_color = (145,121,0) # heart gold 
    text_color = (124,10,2) # barn red
    fill_color = (0,0,0) # black
    gameover_color = (255,255,255) # white
    highlight_color = (200,200,200) # darker white
    sidebar_width = 300 

    def __init__(self : Applet, window_frame : tuple, square_frame : tuple) -> None:
        pygame.init()
        self.window_frame = window_frame
        self.square_frame = square_frame
        self.create_display()
        self.game_loop()

    def create_display(self : Applet) -> None:
        self.surface_display = pygame.display.set_mode(self.window_frame)
        pygame.display.set_caption('Snake')

    def display_title(self : Applet, sidebar_width : int) -> int:
        
        fontObj = pygame.font.SysFont('comicsansms', 72)
        textSurfaceObj = fontObj.render('SNAKE', True, (255,102,0))
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (self.window_frame[0] - sidebar_width, 0)

        self.surface_display.blit(textSurfaceObj, textRectObj)
        return fontObj.get_height()

    def display_score(self : Applet, sidebar_width : int, font_height : int) -> int: 
        
        fontObj = pygame.font.SysFont('comicsansms', 36)
        textSurfaceObj = fontObj.render(f'Score: {self.score}', True, self.text_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.topleft = (self.window_frame[0] - sidebar_width, font_height + int(font_height/2))

        self.surface_display.blit(textSurfaceObj, textRectObj)
        return fontObj.get_height()

    def display_howToPlay(self : Applet, sidebar_width : int, font_height : int) -> None:

        def display_text(content : str, font_height : int) -> tuple:

            fontObj = pygame.font.SysFont('comicsansms', 36)
            textSurfaceObj = fontObj.render(content, True, self.text_color) 
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.topleft = (self.window_frame[0] - sidebar_width, font_height)

            self.surface_display.blit(textSurfaceObj, textRectObj)

            font_height += fontObj.get_height()
            return font_height, fontObj

        def display_images(content : str, font_height : int, fontObj : pygame.font) -> int:

            img = pygame.image.load(content)
            textRectObj = img.get_rect()
            self.surface_display.blit(img, (self.window_frame[0] - fontObj.size('To Move:')[0] - self.square_frame[0], font_height))
            font_height += textRectObj.height
            return font_height

        font_height, fontObj = display_text('HOW TO PLAY:', font_height)
        font_height, fontObj = display_text('To Move:', font_height)
        font_height = display_images('wasd keys.png', font_height, fontObj)
        font_height = display_images('arrow keys.png', font_height, fontObj)
        font_height, fontObj = display_text('To Quit:', font_height)
        font_height = display_images('escape key.png', font_height, fontObj)
        display_images('qkey.png', font_height, fontObj)

    def gamebar_seperators(self : Applet, x_val : int, y_val: int) -> None:
        pygame.draw.line(self.surface_display, self.sidebar_sep_color, (x_val,y_val+int(y_val/4)), (self.window_frame[0],y_val+int(y_val/4)), 5)

    def side_bar(self : Applet) -> None:

        sidebar_topx = self.window_frame[0] - self.sidebar_width
        sidebar_topy = 0

        sidebar = pygame.draw.rect(self.surface_display, self.sidebar_color, (sidebar_topx, sidebar_topy, self.sidebar_width, self.window_frame[1]))

        font_height = self.display_title(sidebar.width-20)
        self.gamebar_seperators(sidebar_topx, font_height)

        font_height += self.display_score(sidebar.width-20, font_height - 15)
        self.gamebar_seperators(sidebar_topx, font_height)

        self.display_howToPlay(sidebar.width-20, font_height + 40)

    def display_gameover(self : Applet) -> bool:
        
        fontObj = pygame.font.SysFont('timesnewroman', 72)
        textSurfaceObj = fontObj.render('GAME OVER', True, self.gameover_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (int(self.window_frame[0]/2), int(self.window_frame[1]/2))

        self.surface_display.blit(textSurfaceObj, textRectObj)

        def display_tryagain(textRectObj : pygame.Rect) -> bool:
            
            display_again = False
            x_display = textRectObj.bottomleft[0]+int(textRectObj.width/4)
            y_display = textRectObj.bottomleft[1]+int(self.square_frame[1]/2)
            width = height = int(textRectObj.width/2)

            mouse = pygame.mouse.get_pos()

            if x_display + width > mouse[0] > x_display and \
               y_display + height > mouse[1] > y_display:

                rectObj = pygame.draw.rect(self.surface_display, self.highlight_color, (x_display, y_display, width, height))

                for event in pygame.event.get([MOUSEBUTTONDOWN]):
                   display_again = True

            else:
                rectObj = pygame.draw.rect(self.surface_display, self.gameover_color, (x_display, y_display, width, height))

            fontObj = pygame.font.SysFont('timesnewroman', 36)
            textSurfaceObj = fontObj.render('RESTART', True, self.fill_color)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = rectObj.center

            self.surface_display.blit(textSurfaceObj, textRectObj)
            return display_again

        return display_tryagain(textRectObj)

    def game_loop(self : Applet) -> None:    
         
        apple = Apple(self.window_frame, self.square_frame, self.sidebar_width)
        snake = Snake(self.window_frame, self.square_frame, self.sidebar_width)

        fpsClock = pygame.time.Clock()
        user_quits = False
        loop_again = False
        collided = False

        while not user_quits:

            pygame.time.delay(15)

            for event in pygame.event.get([QUIT, KEYDOWN, KEYUP]):
                if event.type == QUIT or event.key == K_ESCAPE or event.key == K_q:
                    user_quits = True

            self.surface_display.fill(self.fill_color)

            if not snake.hit_boundary(self.window_frame, self.square_frame, self.sidebar_width): # and not snake.hit_self():

                drawn_snake = snake.draw_snake(self.surface_display, self.square_frame, self.score, collided)
                snake.update_snake_coord()
                collided = False

                self.side_bar()

                drawn_apple = apple.draw_food(self.surface_display, self.square_frame)

                if drawn_snake.colliderect(drawn_apple):
                    apple.clear_drawn_food(self.surface_display, self.square_frame)
                    
                    while(True):
                        updated_apple = apple.update_apple_coord(self.surface_display, self.window_frame, self.square_frame, self.sidebar_width)
                        vals = snake.snake_parts.values()
                        rect_list = [list(vals)[index][0] for index in range(len(list(vals)))]

                        if any(list(filter(lambda snake_part : updated_apple.colliderect(snake_part), rect_list))): 
                            continue
                        else:
                            break

                    self.score += 1
                    collided = True

            else:
                loop_again = self.display_gameover()

            fpsClock.tick(self.fps)
            pygame.display.update()

            if loop_again:
                self.score = 0
                self.game_loop()

        pygame.quit()
        quit()

Applet((1440,900), (40,40))