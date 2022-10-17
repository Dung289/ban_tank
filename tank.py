from turtle import screensize
import pgzrun
import random


WIDTH = 800
HEIGHT = 600
SIZE_TANK = 25
walls = []
bullets = []
bullets_holdoff = 0
enemy_move_count = 0
enemy_bullets = []
game_over = False
enemies = []
# setup player 

player = Actor('tank_blue')
player.pos = (WIDTH/2, HEIGHT-SIZE_TANK)
player.angle = 90

#setup enemy
for i in range(6):
    enemy = Actor('tank_red')
    enemy.x = i * 100 + 100
    enemy.y = SIZE_TANK
    enemy.angle = 270
    enemies.append(enemy)

# setup background and object

background = Actor('grass')
for x in range(16):
    for y in range(1, 10):
        if random.randint(0, 100) < 50:
            wall = Actor('wall')
            wall.x = x * 50 + SIZE_TANK
            wall.y = y * 50 + SIZE_TANK
            walls.append(wall)
            
def player_set():
    original_x = player.x
    original_y = player.y
    if keyboard.A:
        player.x = player.x - 2
        player.angle = 180
    if keyboard.D:
        player.x = player.x + 2
        player.angle = 0
    if keyboard.W:
        player.y = player.y - 2
        player.angle = 90
    if keyboard.S:
        player.y = player.y + 2
        player.angle = 270
    if player.collidelist(walls) != -1:
        player.x = original_x
        player.y = original_y
    if player.x < SIZE_TANK or player.x > WIDTH - SIZE_TANK:
        player.x = original_x
    if player.y < SIZE_TANK or player.y > HEIGHT - SIZE_TANK:
        player.y = original_y
        
def player_bullets_set():
    global bullets_holdoff
    if bullets_holdoff == 0: 
        if keyboard.space:
            bullet = Actor('bulletblue2')
            bullet.angle = player.angle
            bullet.pos = player.pos 
            if bullet.angle == 0:
                bullet.x += SIZE_TANK/2 + 10
            if bullet.angle == 180:
                bullet.x -= SIZE_TANK/2 + 10
            if bullet.angle == 90:
                bullet.y -= SIZE_TANK/2 + 10
            if bullet.angle == 270:
                bullet.y += SIZE_TANK/2 + 10
            bullets.append(bullet)
            bullets_holdoff = 30
    else:
        bullets_holdoff -= 1
    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x += 5
        if bullet.angle == 180:
            bullet.x -= 5
        if bullet.angle == 90:
            bullet.y -= 5
        if bullet.angle == 270:
            bullet.y += 5
    for bullet in bullets:
        walls_index = bullet.collidelist(walls)
        if walls_index != -1:
            sounds.gun9.play()
            del walls[walls_index]
            bullets.remove(bullet)
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)  
        enemies_index = bullet.collidelist(enemies)
        if enemies_index != -1:
            sounds.exp.play()
            del enemies[enemies_index]
            bullets.remove(bullet)

def enemy_set():
    global enemy_move_count, bullets_holdoff
    for enemy in enemies:
        original_x = enemy.x
        original_y = enemy.y
        choice = random.randint(0 , 2)
        if enemy_move_count > 0:
            enemy_move_count -= 1
            if enemy.angle == 0:
                enemy.x += 3
            elif enemy.angle == 180:
                enemy.x -= 3
            elif enemy.angle == 90:
                enemy.y -= 3
            elif enemy.angle == 270:
                enemy.y += 3
            if enemy.x < SIZE_TANK or enemy.x > WIDTH - SIZE_TANK:
                enemy.x = original_x
            if enemy.y < SIZE_TANK or enemy.y > HEIGHT - SIZE_TANK:
                enemy.y = original_y 
                enemy_move_count = 0
            if enemy.collidelist(walls) != -1:
                enemy.x = original_x
                enemy.y = original_y
                enemy_move_count = 0
        elif choice == 0:
            enemy_move_count = 30
        elif choice == 1:
            enemy.angle = 90 *random.randint(0, 3)
        else:
            if bullets_holdoff == 0:
                bullet = Actor('bulletred2')
                bullet.angle = enemy.angle
                bullet.pos = enemy.pos
                enemy_bullets.append(bullet)
                bullets_holdoff = 20
            else:
                bullets_holdoff -= 1

def enemy_bullets_set():
    global enemies, game_over
    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x += 5
        if bullet.angle == 180:
            bullet.x -= 5
        if bullet.angle == 90:
            bullet.y -= 5
        if bullet.angle == 270:
            bullet.y += 5

        for bullet in enemy_bullets:
            walls_index = bullet.collidelist(walls)
            if walls_index != -1:
                sounds.gun9.play()
                del walls[walls_index]
                enemy_bullets.remove(bullet)
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                enemy_bullets.remove(bullet)  
            if bullet.colliderect(player):
                sounds.exp.play()
                game_over = True
        
def update():
    player_set()
    player_bullets_set()
    enemy_set()
    enemy_bullets_set()

def draw():
    if game_over == True:
        screen.fill((0,0,0))
        screen.draw.text('YOU LOSE!', (260,250), color = (255,255,255), fontsize = 100)
    elif len(enemies) == 0:
        screen.fill((0,0,0))
        screen.draw.text('YOU WIN!', (260,250), color = (255,255,255), fontsize = 100)
    else:
        background.draw()
        player.draw()
        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in enemy_bullets:
            bullet.draw()
pgzrun.go()