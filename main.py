import pygame
import math
import random
from pygame import mixer  # Helps to deal with music

# initialize the pygame library
pygame.init()

# creating screen and entering value of width and height into it
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('1876.jpg')

# Background sound
mixer.music.load('background.wav')  # load is used because we want to play music for long time
mixer.music.play(-1)  # to play sound in loop

# Title and Icon
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# Player (loading player)
playerImg = pygame.image.load('player.png')
playerX = 370  # X coordinate of player position
playerY = 480  # Y coordinate of player position
playerX_change = 0

# Enemy (loading enemy)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('pink_alien.png'))
    enemyX.append(random.randint(0, 736))  # random enemy position x-axis between 0 to 800
    enemyY.append(random.randint(50, 150))  # random enemy position y-axis
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet (loading bullet)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready means bullet currently not visible
# fire means bullet is currently moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Font style and size
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):  # For text first we need to render then we blit it on the screen
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))  # text, text, True, Colour
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # Drawing image of player on screen


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True  # Collision occoured
    else:
        return False  # Collision didn't occoured


# Holding screen for a long time (until cross button is pressed) [Game loop]
running = True
while running:

    # Colour on screen
    screen.fill((255, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check which keystroke is pressed
        if event.type == pygame.KEYDOWN:  # keydown means presssing of a key
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # Getting current position of the spaceship
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # releasing a key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change  # changing the x coordinate for movement
    # Creating boundries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # For collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # Calling player over screen
    show_score(textX, textY)
    pygame.display.update()  # To update any change in the display
