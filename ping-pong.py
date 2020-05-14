import pygame, sys, random
from detector import *

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        
    if ball.left <= 0: 
        player_score += 1
        score_time = pygame.time.get_ticks()
        
    if ball.right >= screen_width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()
    
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        
def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
        
def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width/2, screen_height/2)
    
    if current_time - score_time < 700: 
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (screen_width/2 -10, screen_height/2 + 20))
    
    if 700 < current_time - score_time < 1400:
        number_one = game_font.render("2", False, light_grey)
        screen.blit(number_one, (screen_width/2 -10, screen_height/2 + 20))
    
    if 1400 < current_time - score_time < 2100:
        number_two = game_font.render("1", False, light_grey)
        screen.blit(number_two, (screen_width/2 -10, screen_height/2 + 20))
    
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 13 * random.choice((1,-1))
        ball_speed_x = 13 * random.choice((1,-1))
        score_time = None

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 640 
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,140)

# Colors
light_grey = (230,230,230)
bg_color = pygame.Color(0, 0, 0)

# Game Variables
ball_speed_x = 13 * random.choice((1,-1))
ball_speed_y = 13 * random.choice((1,-1))
player_speed = 0
opponent_speed = 13

#Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 24)
pause_text = pygame.font.SysFont('Consolas', 32).render('Hand Not Found', False, (255, 255, 255))

#Score Timer
score_time = True

# get videocapture object, with game window dimensions
cap = init_cap(screen_width, screen_height)

while True:
    # detect hand and get its coordinates
    hand_pos = get_pos(cap)

    if hand_pos:

        # if negative returned, close window
        if hand_pos < 0:
            pygame.quit()
            sys.exit()

        # set player position based on hand coordinates
        else:
            player.y = hand_pos - 60

    # if hand is not detected, pause the game 
    else:
        screen.blit(pause_text, (400, 300))   ############################### СЮДА НАДО СДЕЛАТЬ ТЕКСТ ПАУЗЫ
        continue

    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Game logic
    ball_animation()
    player_animation()
    opponent_ai()
    
    # Visuals 
    screen.fill(bg_color)
    
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    
    if score_time:
        ball_start()
        
    
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (350, 10))
    
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (280, 10))
    
    # Updating the window 
    pygame.display.flip()
    clock.tick(60)

