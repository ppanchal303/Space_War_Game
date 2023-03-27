import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 500
WIN  = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

bgcolor = (108, 116, 118)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
# BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont('arial black', 26)
WINNER_FONT = pygame.font.SysFont('arial black', 100)

FPS = 60
VEL = 4
BULLET_VEL = 5
MAX_BULLETS = 3
ship_width = 46
ship_height = 38

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Yellow Spaceship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (ship_width, ship_height)), 90)

# # Random box
# BOX = pygame.Rect((WIDTH//4 - ship_width/2), (250 - ship_height/2), 38, 46)
# BOX2 = pygame.Rect((3*WIDTH//4 - ship_width/2), (250 - ship_height/2), 38, 46)

# Red Spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (ship_width, ship_height)), 270)

# Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

# Window draw function
def draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health, winner_text):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # pygame.draw.rect(WIN, BLUE, BOX)
    # pygame.draw.rect(WIN, BLUE, BOX2)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))      # displays the yellow ship
    WIN.blit(RED_SPACESHIP, (red.x, red.y))     # displays the red ship
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    red_health_text.set_alpha(192)
    yellow_health_text.set_alpha(192)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()     # updates the display



# Handle the yellow ship movement
def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:               # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width < BORDER.x:     # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y > 0:               # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height < HEIGHT - 10:          # DOWN
        yellow.y += VEL

# Handle the red ship movement
def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > BORDER.x + BORDER.width + 5:     # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH + 10:     # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y > 0:     # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height < HEIGHT - 10:     # DOWN
        red.y += VEL

# Handle bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + bullet.width < 0:
            red_bullets.remove(bullet)

# Draw the winner message
def draw_winner(text):
    game_end_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(game_end_text, (WIDTH//2 - game_end_text.get_width()//2, HEIGHT//2 - game_end_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


# The main fuction where everthing is executed
def main():
    yellow = pygame.Rect((WIDTH//4 - ship_width/2), (HEIGHT//2 - ship_height/2), ship_width, ship_height)
    red = pygame.Rect((3*WIDTH//4 - ship_width/2), (HEIGHT//2 - ship_height/2), ship_width, ship_height)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)     # sets the internal clock to control the FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       # capture the event of closing the window, not doing this won't close the window and we will have to force quit
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width - 6, yellow.y + yellow.height//2 + 1, 10, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 10, red.y + red.height//2 + 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health == 0:
            winner_text = "Yellow Wins!"

        if yellow_health == 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)        # Someone won
            break
        
        # print(yellow_bullets, red_bullets)
        keys_pressed = pygame.key.get_pressed()     # takes the input of the keys pressed
        handle_yellow_movement(keys_pressed, yellow)        # calls the yellow movement function
        handle_red_movement(keys_pressed, red)      # calls the red movement function

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health, winner_text)       # calls the draw function

    main()

# This command is used so that the main runs only if this file is opened directly and not called/referenced by any other file
if __name__ == "__main__":
    main()