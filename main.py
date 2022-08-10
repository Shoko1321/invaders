import math
import pygame
import random
from pygame import mixer
import sys
import os


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((1000, 800))

#Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display .set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',50)
textX = 10
textY = 10

# PLayer
playerImg = pygame.image.load('player.png')
playerX = 470
playerY = 680
playerX_change = 0
# Kill count
kc = 0


#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,935))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)
    

#laser

#ready - you cant see the bullet on screen

#Fire - the bullet is currently moving
laserImg = pygame.image.load('laser.png')
laserX = playerX
laserY = 680
laserx_change = 0
laserY_change = 10
laser_state = 'ready'




#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True,(245,237,37))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255,0,0))
    screen.blit(over_text,(350,450))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_laser(x,y):
    global laser_state
    laser_state = 'fire'
    screen.blit(laserImg, (x + 16, y+ 10))

def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX,2)) + (math.pow(enemyY - laserY,2)))
    if distance <27:
        return True
    else:
        return False
# Game loop
running = True
while running:
                #RBG value
    screen.fill((0,0,0)) 
    #Background Image
    screen.blit(background,(0,0))
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state == 'ready':
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0



    playerX += playerX_change

    #PLayer boundary check
    if playerX <=0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    #Enemy movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 640:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 3
            if score_value >= 200:
                enemyX_change[i] = 10
            elif score_value >= 100:
                enemyX_change[i] = 5
            elif score_value >= 50:
                enemyX_change[i] = 4 
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -3
            if score_value >= 200:
                enemyX_change[i] = -10            
            elif score_value >= 100:
                enemyX_change[i] = -5
            elif score_value >= 50:
                enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        #Collision
        collision = isCollision(enemyX[i],enemyY[i],laserX,laserY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            laserY = 680
            laser_state = 'ready'
            score_value += 10
            kc += 1
            print(kc)
            if score_value >= 150:
                score_value += 20
            enemyX[i] = random.randint(0,935)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i], enemyY[i], i)    
        
           
    #Laser Movement
    if laserY <= 0:
        laserY = 680
        laser_state = 'ready'

    if laser_state == 'fire':
        fire_laser(laserX, laserY)
        laserY -= laserY_change




    enemy(enemyX[i], enemyY[i], i)
    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
