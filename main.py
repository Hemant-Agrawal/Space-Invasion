import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('Images\\space-bg.png')
mixer.music.load('Sound\\background.wav')
mixer.music.play(-1)

pygame.display.set_caption('Space Invasion')
icon = pygame.image.load('Images\\globe.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('Images\\spaceship.png')
playerX, playerY = 370, 480
playerXchange, playerYchange = 0, 0

enemyImg = pygame.image.load('Images\\alien.png')
enemyX, enemyY = random.randint(0, 800), random.randint(50, 150)
enemyXchange, enemyYchange = 2, 40

blastImg = pygame.image.load("Images\\explosion.png")

bulletImg = pygame.image.load('Images\\bullet.png')
bulletX, bulletY = 0, 480
bulletYchange = 3
bullet_state = 'ready'

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX, textY = 10, 10


def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 16, y + 3))


def isCollision():
    distance = math.sqrt((enemyX-bulletX)**2 + (enemyY-bulletY)**2)
    if distance < 32:
        return True
    return False


running = True
while running:
    screen.fill((128, 128, 128))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -3
            if event.key == pygame.K_RIGHT:
                playerXchange = 3
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound = mixer.Sound("Sound\\laser.wav")
                bullet_sound.play()
                bulletX = playerX
                bulletY = playerY
                bullet_state = 'fire'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange
    if bulletY <= 0:
        bullet_state = 'ready'
    if isCollision():
        explosion_sound = mixer.Sound("Sound\\explosion.wav")
        explosion_sound.play()
        score_value += 1
        bullet_state = 'ready'
        enemyX, enemyY = random.randint(0, 735), random.randint(25, 150)
        bulletX, bulletY = playerX, playerY

    playerX += playerXchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyXchange
    if enemyX <= 0:
        enemyXchange = 2
        enemyY += enemyYchange
    if enemyX >= 736:
        enemyXchange = -2
        enemyY += enemyYchange

    if enemyY > 400:
        game_over_font = pygame.font.Font('freesansbold.ttf', 72)
        game_over_text = game_over_font.render('GAME OVER', True, (255, 255, 255))
        screen.blit(game_over_text, (220, 230))
        enemyY = 900
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)

    pygame.display.update()
