
import pygame,sys, time, random, os, math
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 960
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2)
BLUE = (0, 0, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (125,0,225)
VEL = 5
FIRERATE = 50
E_FIRERATE = 500
playerbullets = []
bullets = []
enemies = []

WIN_FONT = pygame.font.SysFont('comic sans', 100, True, True)
WIN_FONT = pygame.font.SysFont('arial', 60, True)
BULLETFIRESOUND = pygame.mixer.Sound('bullethell/misc/ATTACK3.wav')
BULLETFIRESOUND.set_volume(0.1)
DEATHSOUND = pygame.mixer.Sound("bullethell/misc/DEAD.wav")



pygame.display.set_caption("ProjeCturne")

#pygame.display.set_icon('images/BG+UI/icon.png') 
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('bullethell/images/BG+UI/main_background-1.png')
        self.image = pygame.transform.scale(self.image, (800, 920))
        #self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect(WIDTH / 2 - 600 ,HEIGHT / 2 - 460, 800, 920)
    def draw(self):
        #WIN.blit(self.image, ((WIDTH / 2) - 600 ,(HEIGHT / 2) - 460))
        WIN.blit(self.image, (self.rect.x, self.rect.y) )

class ForegroundThingy():

    def __init__(self, background):
        self.foregroundlist = []
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x, background.rect.y - 40, 800, 40))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x - 40, background.rect.y, 40, 960))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x + 800, background.rect.y, 40, 960))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x, background.rect.y + 920, 800, 40))
        
    def draw(self):
        for i in self.foregroundlist:
            pygame.draw.rect(WIN, BLUE, i)

class Player:


    def __init__(self):
        self.rect = pygame.Rect(450, 900, 30, 30 )
        self.pos = self.rect.center
        self.hitbox = pygame.Rect(*(self.pos), 10, 10)
        self.hp = 5
    


        self.start_time = 0

    def movement_handling(self, background):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]:
            if keys_pressed[pygame.K_LSHIFT]:
                self.rect.x -= VEL / 2
            else:
                self.rect.x -= VEL
        if keys_pressed[pygame.K_RIGHT]:
            if keys_pressed[pygame.K_LSHIFT]:
                 self.rect.x += VEL / 2
            else:
                self.rect.x += VEL
        if keys_pressed[pygame.K_UP]:
            if keys_pressed[pygame.K_LSHIFT]:
                self.rect.y -= VEL / 2
            else:    
                self.rect.y -= VEL
        if keys_pressed[pygame.K_DOWN]:
            if keys_pressed[pygame.K_LSHIFT]:
                self.rect.y += VEL / 2
            else:
                self.rect.y += VEL
        
        self.rect.clamp_ip(background.rect)
        self.hitbox.center = self.rect.center
    def draw(self):
        pygame.draw.circle(WIN, YELLOW, self.rect.center, 13)
        for i in range(self.hp):
            center = (WIDTH - 250) + (i * 50), 300
            pygame.draw.circle(WIN, YELLOW, center, 20)
       # pygame.draw.rect(WIN, RED, self.hitbox)

    def bullet_handling(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_z]:
            if (pygame.time.get_ticks() - self.start_time) >= FIRERATE:
                self.start_time = pygame.time.get_ticks() 
                playerbullets.append(PlayerBullet(self.rect.centerx-10, self.rect.y))
                playerbullets.append(PlayerBullet(self.rect.centerx+10, self.rect.y))
                BULLETFIRESOUND.play() 
               
class PlayerBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-5, y-20, 5, 30)
        self.pos = self.rect.x, self.rect.y
        self.bullet = pygame.image.load(os.path.join('bullethell','images', 'Sprites' , 'bullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (10, 40))
        self.destroy = False

    def update(self):
        self.rect.y -= 15
    def draw(self, surf):
        surf.blit(self.bullet, self.rect)

class Bullet():
    def __init__(self, x, y, player, speed):
        self.bullethbox = pygame.Rect(x, y, 5, 5 )
        self.pos = (x, y)
        mx, my = player.hitbox.center
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
        self.bullet = pygame.image.load(os.path.join('bullethell', 'images', 'Sprites' , 'enemybullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (23, 16))
        self.rotated_bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = speed
    def update(self): 

        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        self.bullethbox.center = self.pos

        bulletrect = self.rotated_bullet.get_rect(center = self.bullethbox.center)

        surf.blit(self.rotated_bullet, bulletrect)
        #pygame.draw.rect(surf, RED, self.bullethbox)

class Bullet_H():
    def __init__(self, x, y, angle, speed):
        self.bullethbox = pygame.Rect(x, y, 16, 16 )
        self.pos = (x, y)
        self.angle = angle - 90
        self.bullet = pygame.image.load(os.path.join('bullethell', 'images', 'Sprites' , 'bigBullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (32, 32))
        self.speed = speed
    def update(self): 
        self.pos = calculate_angle(self.pos, self.speed, -self.angle)
        self.bullethbox.center = round(self.pos[0]), round(self.pos[1])

    def draw(self, surf):
        self.bullethbox.center = self.pos

        bulletrect = self.bullet.get_rect(center = self.bullethbox.center)
        

        surf.blit(self.bullet, bulletrect)
        #pygame.draw.rect(surf, RED, self.bullethbox)

class Enemy():
    def __init__(self, x, y, player, firerate, bulletVel, xvel=0, yvel=0, hp=20, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.firerate = firerate
        self.bulvel = bulletVel
        self.pos = self.rect.center
        self.start_time = 0
        self.hp = hp
        self.player = player
        self.xvel = xvel
        self.yvel = yvel
        self.isShooting = isShooting
        run = True
    
        
    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        self.pos = self.rect.center
        if self.isShooting == True:
            if (pygame.time.get_ticks() - self.start_time) >= self.firerate:
                self.start_time = pygame.time.get_ticks() 
                bullets.append(Bullet(*(self.pos), self.player, self.bulvel))
        
    def draw(self, surf):
        pygame.draw.circle(surf, PURPLE, (self.pos), 20)

class Enemy_2():
    def __init__(self, x, y, player, moveTime, bulletVel, hp, firerate, xvel=0, yvel=0, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.moveTime = moveTime*1000
        self.bulvel = bulletVel
        self.pos = self.rect.center
        self.start_time = 0
        self.start_time2 = 0
        self.clock = pygame.time.Clock()
        self.hp = hp
        self.firerate = firerate
        self.player = player
        self.xvel = xvel
        self.yvel = yvel
        self.isShooting = isShooting
        self.fireangle = 0
        run = True
    
        
    def update(self):
        t = pygame.time.get_ticks() / 4000
        fireangle = 45*math.sin(t)


        time_delta = self.clock.tick(FPS)
        self.start_time2 += time_delta
        if self.start_time2 < self.moveTime:
            self.pos = self.rect.center
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            
        else:
            if self.isShooting == True:
                if (pygame.time.get_ticks() - self.start_time) >= self.firerate:
                    self.start_time = pygame.time.get_ticks() 
                    bullets.append(Bullet(*(self.pos), self.player, self.bulvel))
            elif (pygame.time.get_ticks() - self.start_time) >= self.firerate:
                    self.start_time = pygame.time.get_ticks() 
                    for angle in range(0, 360, 10):
                        bullets.append(Bullet_H(*self.pos, angle + fireangle, self.bulvel))
    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (self.pos), 20)
                        
                        
class Enemy_3():
    def __init__(self, x, y, player, moveTime, bulletVel, hp, firerate, step=5,range=(0,0), angle=0, xvel=0, yvel=0, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.range = range
        self.angle = angle
        self.moveTime = moveTime*1000
        self.bulvel = bulletVel
        self.step = step
        self.pos = self.rect.center
        self.start_time = 0
        self.start_time2 = 0
        self.clock = pygame.time.Clock()
        self.hp = hp
        self.firerate = firerate
        self.player = player
        self.xvel = xvel
        self.yvel = yvel
        self.isShooting = isShooting
        self.fireangle = 0
        run = True
    
        
    def update(self):
        t = pygame.time.get_ticks() / 4000
        fireangle = 10*math.sin(t)


        time_delta = self.clock.tick(FPS)
        self.start_time2 += time_delta
        if self.start_time2 < self.moveTime:
            self.pos = self.rect.center
            self.rect.x += self.xvel
            self.rect.y += self.yvel
        else:    
            if (pygame.time.get_ticks() - self.start_time) >= self.firerate:
                self.start_time = pygame.time.get_ticks() 
                if self.isShooting == True:
                    bullets.append(Bullet_H(*self.pos, self.angle, self.bulvel))
                elif self.isShooting == False:
                    self.start_time = pygame.time.get_ticks() 
                    for angle in range(self.range[0], self.range[1], self.step):
                        bullets.append(Bullet_H(*self.pos, angle + fireangle, self.bulvel))
    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (self.pos), 20)
        
class Enemy_4():
    def __init__(self, x, y, player, moveTime, bulletVel, hp, firerate, xvel=0, yvel=0, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.moveTime = moveTime*1000
        self.bulvel = bulletVel
        self.pos = self.rect.center
        self.start_time = 0
        self.start_time2 = 0
        self.clock = pygame.time.Clock()
        self.hp = hp
        self.firerate = firerate
        self.player = player
        self.xvel = xvel
        self.yvel = yvel
        self.isShooting = isShooting
        self.fireangle = 0
        run = True
    
        
    def update(self):
        t = pygame.time.get_ticks() / 500
        fireangle = 45*math.sin(t)


        time_delta = self.clock.tick(FPS)
        self.start_time2 += time_delta
        if self.start_time2 < self.moveTime:
            self.pos = self.rect.center
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            
        else:
            
            if (pygame.time.get_ticks() - self.start_time) >= self.firerate:
                self.start_time = pygame.time.get_ticks() 
                    
                bullets.append(Bullet_H(*self.pos, fireangle, self.bulvel))
                self.fireangle += 10
                    

    def draw(self, surf):
        pygame.draw.circle(surf, RED, (self.pos), 20)            
            
            


        
        
    


def calculate_angle(startxy, speed, angle):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle))
    return startxy + move_vec

def main():
    global clock
    clock = pygame.time.Clock()

    titleScreen(WIN)
    gameLoop()
    draw_win()



def titleScreen(WIN):
    newGame = pygame.image.load("bullethell/images/BG+UI/new_game_button.png")
    closeGame = pygame.image.load("bullethell/images/BG+UI/exit_button.png")
    buttons = [newGame,closeGame]
    loopContinues = True
    selected = buttons[0]
    brighten = 128
    newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
    dim = 128
    while loopContinues:
        
        #we do a little event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopContinues = False
                sys.exit()
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != buttons[0]:
                        #if you press up and aren't on newGame, that means you're on closeGame. This moves you back to newGame.
                        selected = buttons[0]
                        newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
                        closeGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB)  
                    elif selected != buttons[1]:
                        #if you press up and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                        closeGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        newGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_DOWN:
                    if selected != buttons[1]:
                        #if you press down and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                        closeGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        newGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                    elif selected != buttons[0]:
                        #if you press down and aren't on newGame, that means you're on closeGame. This moves you back to newGame.
                        selected = buttons[0]
                        newGame.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
                        closeGame.fill((dim, dim, dim), special_flags=pygame.BLEND_RGB_SUB) 
                if event.key == pygame.K_z:
                        if selected == buttons[0]:
                            #play select sfx
                            gameLoop()
                        elif selected == buttons[1]:
                            #play select sfx
                            time.sleep(1)
                            pygame.quit()
                            sys.exit()
                        #note to self: add a thing that makes the currently selected button light up (maybe by increasing contrast?)
        WIN.blit(newGame, (WIDTH/2 - 130, HEIGHT/2 - 270))
        WIN.blit(closeGame, (WIDTH/2 - 130, HEIGHT/2 + 100))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.update()
                        

class GameController():

    def __init__(self, background, player):
        self.now = 0
        self.now2 = 0
        self.gameState = 0
        self.passedTime = 0
        self.bounds = background.rect
        self.player = player
        self.clock = pygame.time.Clock()
        self.spawned = False
    
            
    def enemypattern_1(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta    
        if self.passedTime < 5000:
            if (pygame.time.get_ticks() - self.now2) >= 500:
                    self.now2 = pygame.time.get_ticks()
        
                    enemies.append(Enemy(self.bounds.x + 100, 0, self.player, 0, 0,2, 3, 2))
                    enemies.append(Enemy(self.bounds.x + 700, 0, self.player, 0, 0,-2, 3, 2))
                    enemies.append(Enemy(self.bounds.x + 100, 0, self.player, 0, 0,2, 3, 2))
                    enemies.append(Enemy(self.bounds.x + 700, 0, self.player, 0, 0, -2, 3, 2))
        else:
            if len(enemies) == 0:
                self.gameState = 1
                self.passedTime = 0
                print('next phase!')
    def enemypattern_2(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta

        randomx = random.randint(self.bounds.x + 100, 700)
        if self.passedTime < 10000:
            if (pygame.time.get_ticks() - self.now) >= 2000:
                self.now = pygame.time.get_ticks()
                if len(enemies) <= 5:
                    enemies.append(Enemy(randomx, 0, self.player, 1000 , 3 , 0, 0.5, 20,True))
        else:
            if len(enemies) == 0:
                self.gameState += 1
                self.passedTime = 0
                print('next phase!')
    def enemypattern_3(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if len(enemies) == 0 and self.spawned == False:
            enemies.append(Enemy_2(x=self.bounds.x + 400, y=0, 
                                   player=self.player, 
                                   moveTime=1, 
                                   bulletVel=3, 
                                   hp=50, 
                                   firerate=1000 , 
                                   xvel=0, yvel=3))
            self.spawned = True
        else:
            if len(enemies) == 0:
                self.gameState += 1
                self.passedTime = 0
                print('next phase!')
                self.spawned = False
    def enemypattern_4(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if self.passedTime < 15000:
            if (pygame.time.get_ticks() - self.now) >= 2000:
                self.now = pygame.time.get_ticks()
                enemies.append(Enemy(self.bounds.x + 100, 0, self.player, 800 , 5 , 0, 0.5, 5,True))
                enemies.append(Enemy(self.bounds.x + 700, 0, self.player, 800 , 5 , 0, 0.5, 5,True))
        else:
            if len(enemies) == 0:
                self.gameState += 1
                self.passedTime = 0
                print('next phase!')
    def enemypattern_5(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if self.spawned == False:
            enemies.append(Enemy_2(x=self.bounds.x + 100, y=0, 
                                   player=self.player, 
                                   moveTime=1, 
                                   bulletVel=3, 
                                   hp=50, 
                                   firerate=1000 , 
                                   xvel=0, yvel=2))
            self.spawned = True
        elif self.passedTime < 25000:
            if (pygame.time.get_ticks() - self.now) >= 2000 and len(enemies)<= 3:
                self.now = pygame.time.get_ticks()
                enemies.append(Enemy_2(x=random.randint(self.bounds.x + 300, 700), y=0, 
                                   player=self.player, 
                                   moveTime=1, 
                                   bulletVel=3, 
                                   hp=20, 
                                   firerate=700 , 
                                   xvel=0, yvel=2, isShooting=True))
                enemies.append(Enemy_2(x=random.randint(self.bounds.x + 300, 700), y=0, 
                                   player=self.player, 
                                   moveTime=1, 
                                   bulletVel=3, 
                                   hp=20, 
                                   firerate=700, 
                                   xvel=0, yvel=2, isShooting=True))
        else:
            enemies.clear()
            if len(bullets) == 0:
                self.gameState += 1
                self.passedTime = 0
                self.spawned = False
                print('next phase!')

            
    def enemypattern_6(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if self.passedTime < 20000:
            if (pygame.time.get_ticks() - self.now) >= 3000:
                self.now = pygame.time.get_ticks()
                if self.spawned == False:
                    for i in range(100, 800, 100):
                        enemies.append(Enemy_3(self.bounds.x + i, y=0, 
                                            player=self.player, 
                                            moveTime=0.5, 
                                            bulletVel=3, 
                                            hp=20, 
                                            firerate=500, 
                                            step= 1,
                                            range= (45,50),
                                            angle= 0,
                                            xvel=0, yvel=2, isShooting=True))
                        enemies.append(Enemy_3(x=self.bounds.x + 100, y=0, 
                                    player=self.player, 
                                    moveTime=1, 
                                    bulletVel=3, 
                                    hp=50, 
                                    firerate=2000 ,
                                    range= (0, 90),
                                    step= 10, 
                                    xvel=0, yvel=2))
                        enemies.append(Enemy_3(x=self.bounds.x + 700, y=0, 
                                    player=self.player, 
                                    moveTime=1, 
                                    bulletVel=3, 
                                    hp=50, 
                                    firerate=2500 ,
                                    range= (-90, 0),
                                    step= 10, 
                                    xvel=0, yvel=2))
                        enemies.append(Enemy_2(x=self.bounds.x + 50, y=0, 
                                    player=self.player, 
                                    moveTime=1, 
                                    bulletVel=3, 
                                    hp=50, 
                                    firerate=800 , 
                                    xvel=0, yvel=1,
                                    isShooting=True))
                        enemies.append(Enemy_2(x=self.bounds.x + 750, y=0, 
                                    player=self.player, 
                                    moveTime=1, 
                                    bulletVel=3, 
                                    hp=50, 
                                    firerate=800 , 
                                    xvel=0, yvel=1,
                                    isShooting=True))
                    self.spawned = True

        

        else:
            enemies.clear()
            if len(bullets) == 0:
                self.gameState += 1
                self.passedTime = 0
                self.spawned = False
                print('next phase!')
    def enemypattern_7(self):
        self.now = 0
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if self.passedTime < 30000:
            if self.spawned == False:
                enemies.append(Enemy_2(x=self.bounds.x + 100, y=0, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=2, 
                                        hp=10, 
                                        firerate=1500 , 
                                        xvel=0, yvel=3))
                enemies.append(Enemy_4(x=self.bounds.x + 300, y=-130, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=3, 
                                        hp=5, 
                                        firerate=250 , 
                                        xvel=0, yvel=3))
                enemies.append(Enemy_2(x=self.bounds.x + 350, y=0, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=3, 
                                        hp=5, 
                                        firerate=250 , 
                                        xvel=0, yvel=3))
                                        
                enemies.append(Enemy_2(x=self.bounds.x + 450, y=0, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=3, 
                                        hp=5, 
                                        firerate=250 , 
                                        xvel=0, yvel=3))
                enemies.append(Enemy_4(x=self.bounds.x + 500, y=-130, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=3, 
                                        hp=5, 
                                        firerate=250 , 
                                        xvel=0, yvel=3))
                enemies.append(Enemy_2(x=self.bounds.x + 700, y=0, 
                                        player=self.player, 
                                        moveTime=1, 
                                        bulletVel=2, 
                                        hp=10, 
                                        firerate=1500 , 
                                        xvel=0, yvel=3))
                self.spawned = True
            
            elif len(bullets) > 600:
                    enemies.clear()
            elif len(enemies) == 0 and len(bullets) < 300:
                self.spawned = False
        else:
            enemies.clear()
            if len(bullets) == 0:
                self.gameState += 1
                self.passedTime = 0
                self.spawned = False
                print('next phase!')
    def victory(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta
        if self.passedTime < 5000:
            global run
            run = False


            
            
def draw_win():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        winbg = pygame.image.load('bullethell/images/bg+ui/image0.jpg')
        WIN.blit(pygame.transform.scale(winbg, SCREEN.get_rect().size), (0,0))
        draw_text = WIN_FONT.render("You're are winner!", 1, WHITE)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()
                
            
        


            

            


                        

            
def gameOver(WIN):
    overclock = pygame.time.Clock()
    over = True
    timePassed = 0
    while over:
        timePassed += overclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        winbg = pygame.image.load('bullethell/images/bg+ui/gameover.jpg')
        WIN.blit(pygame.transform.scale(winbg, SCREEN.get_rect().size), (0,0))
        draw_text = WIN_FONT.render("DEATH", 1, RED)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2 + 200))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()
        if timePassed > 10000:
           over = False
           pygame.quit()





                        
def gameLoop():
    wintext = ""
    global run
    run = True
    player = Player()
    background = Background()
    controller = GameController(background, player)
    foreground = ForegroundThingy(background)
    global timern
    timern = pygame.time.get_ticks()
    now = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




        WIN.fill(BLUE)
        background.draw()

        if controller.gameState == 0:
            controller.enemypattern_1()
        if controller.gameState == 1:
            controller.enemypattern_2()
        if controller.gameState == 2:
            controller.enemypattern_3()
        if controller.gameState == 3:
            controller.enemypattern_4()
        if controller.gameState == 4:
            controller.enemypattern_5()
        if controller.gameState == 5:
            controller.enemypattern_6()
        if controller.gameState == 6:
            controller.enemypattern_7()
        if controller.gameState == 7:
            controller.victory()
        

        if player.hp <= 0:
            gameOver(WIN)
            run= False


        for bullet in playerbullets:
                bullet.draw(WIN)
                bullet.update()
                if not bullet.rect.colliderect(background.rect):
                    bullet.destory = True
                else:
                    for enemy in enemies:
                        if bullet.rect.colliderect(enemy.rect):
                            bullet.destroy = True
                            enemy.hp -= 1
                if bullet.destroy == True:
                    playerbullets.remove(bullet)




        for bullet in bullets[:]:
            bullet.draw(WIN)
            bullet.update()
            

            if not background.rect.colliderect(bullet.bullethbox):
                bullets.remove(bullet)
            elif bullet.bullethbox.colliderect(player.hitbox):
                bullets.remove(bullet)
                if (pygame.time.get_ticks() - now) >= 200:
                    now = pygame.time.get_ticks()
                    DEATHSOUND.play()
                    player.hp -= 1
            
 

        for enemy in enemies[:]:
            enemy.draw(WIN)
            enemy.update()
            if enemy.hp <= 0:
                enemies.remove(enemy)
            elif enemy.rect.y > HEIGHT:
                enemies.remove(enemy)
        lives_text = WIN_FONT.render("Lives:", 1, WHITE)
        
        foreground.draw()
        player.movement_handling(background)
        player.bullet_handling()
        player.draw()
        WIN.blit(lives_text, (WIDTH - 410, 260))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    
#this should load all the sfx necessary for the game, initialize the player sprite (and set up the hitbox), set up the controls, make the shooting work, and then call a function to load level 1. We should make each level a separate module for convenience rather than keeping them all in 1 file imo                        
                        
while __name__ == "__main__":
    main()

