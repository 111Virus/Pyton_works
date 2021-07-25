import pygame as py
# from pygame import mixer as mix
import random
import math

# Everything happening in the game window is called as event Ex:-pressing quit or shooting e tc.

# Initialize the pygame, creating the game window
py.init()

screen = py.display.set_mode((800, 600))  # This is for the game window size, must put double brackets or it won't work.
background = py.image.load('Background.png')  # For background of the game window

py.display.set_caption("Space Invaders")  # Changing the title of the window

# Change the icon / logo of the game window
img32 = py.image.load('rocket32.png')  # 32x32 size rocket image for icon
py.display.set_icon(img32)

# # Background music
# mixer.music.load('background.wav')
# mixer.music.play(-1)  # '-1' added to play music in loop

# Rocket creation
playerImg = py.image.load('rocket64.png')  # 64x64 size rocket image for the game
playerX = 370  # x-position of the image
playerY = 500  # y-position of the image
playerX_change = 0

# Monster creation
# monsterImg = py.image.load('monster.png')  # 64x64 size rocket image for the game
# # Randomising respawn
# monsterX = random.randint(0, 749)
# monsterY = random.randint(10, 200)
# monsterX_change = 2
# monsterY_change = 40

monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
noOfMonsters = 6

for i in range(noOfMonsters):
    monsterImg.append(py.image.load('monster.png'))
    monsterX.append(random.randint(0, 749))
    monsterY.append(random.randint(10, 200))
    monsterX_change.append(2)
    monsterY_change.append(40)

# Bullet creation
bulletImg = py.image.load('bullet.png')  # 64x64 size rocket image for the game
# Randomising respawn
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
# In 'ready' state bullet won't visible on screen & in 'fire' state bullet is visible and moving
bulletState = "ready"

# score board
score_value = 0
font = py.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

game_over_font = py.font.Font('freesansbold.ttf', 200)


def player(x, y):  # Creation of rocket
    screen.blit(playerImg, (x, y))  # 'blit' method draws the image on the screen in the specified position


def monster(x, y, z):  # Creation of monster
    screen.blit(monsterImg[z], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 24, y + 12))


def isCollision(x1, y1, x2, y2):
    distance = (math.sqrt(math.pow((x1 - x2), 2)) + (math.pow((y1 - y2), 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER....", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


# Game loop
running = True
while running:  # To run through game continuously until quit
    # Everything which has to be displayed continuously will go inside this while loop

    # screen.fill((0, 0, 0))  # Setting background colour of the window using RGB values
    screen.blit(background, (0, 0))

    for event in py.event.get():  # This is to run through all the possible events
        if event.type == py.QUIT:  # To verify whether the 'X' button (quit / close) has been pressed
            running = False  # Close the window

        # Controlling the rocket movement with the keyboard keys
        if event.type == py.KEYDOWN:  # To check if any key is pressed & only if it is either 'a' or 's' we'll get o/p
            if event.key == py.K_a:  # 'a' is for moving left
                playerX_change = -5  # print("'a' key is pressed")
            if event.key == py.K_d:  # 's' is for moving right
                playerX_change = 5  # print("'s' key is pressed")
            if event.key == py.K_SPACE:  # 'spacer' is for shooting bullet
                # To make bullet position absolute and fire the bullet only when the state is "ready"
                if bulletState == "ready":
                    # bulletSound = mixer.Sound('bulletSound.wav')
                    # bulletSound.play()
                    bulletX = playerX  # To make the bullet position absolute
                    fire_bullet(bulletX, bulletY)  # print("'spacer' key is pressed")

        if event.type == py.KEYUP:  # To check whether the pressed key has been released or not
            if event.key == py.K_a or event.key == py.K_d:
                # print("Key has been released")
                playerX_change = 0

    # playerX += .1
    # playerX -= .1
    playerX += playerX_change
    # Creating left boundaries & repositioning the rocket
    if playerX <= -1:
        playerX = -1
    elif playerX >= 740:
        playerX = 740
    player(playerX, playerY)  # Calling the player method to display the rocket on the screen

    for i in range(noOfMonsters):
        # Game Over
        if monsterY[i] > 440:
            for j in range(noOfMonsters):
                monsterY[j] = 2000
            game_over_text()
            break
        monsterX[i] += monsterX_change[i]
        # Creating left boundaries & moving the monster
        if monsterX[i] <= -1:
            monsterX_change[i] = 2
            monsterY[i] += monsterY_change[i]
        elif monsterX[i] >= 740:
            monsterX_change[i] = -2
            monsterY[i] += monsterY_change[i]

        # Collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            # collisionSound = mixer.Sound('collisionSound.wav')
            # collisionllSound.play()
            bulletY = 480
            monsterX[i] = random.randint(0, 749)
            monsterY[i] = random.randint(10, 200)
            bulletState = "ready"
            score_value += 1

        monster(monsterX[i], monsterY[i], i)  # Calling the monster method to display the monster on the screen

    # Bullet movement
    if bulletY <= 0:  # To fire multiple bullets after the first bullet reached Y-axis border
        bulletY = 480
        bulletState = "ready"

    if bulletState == "fire":  # To make the bullet move independently in X-axis
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)

    py.display.update()  # To update the display
