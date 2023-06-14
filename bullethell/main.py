import pygame,sys, time, random, os, math



WIDTH, HEIGHT = 1280, 960
SCREEN = pygame.display.set_mode((WIDTH/2, HEIGHT/2))
WIN = pygame.surface.Surface((WIDTH, HEIGHT))
FPS = 60
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2)
BLUE = (0, 0, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
VEL = 5
FIRERATE = 50
E_FIRERATE = 500
playerbullets = []
bullets = []
enemies = []

pygame.display.set_caption("ProjeCturne")

#pygame.display.set_icon('images/BG+UI/icon.png') 
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #self.image = pygame.Surface((640,480))
        #self.image.fill(BLACK)
        #self.image = pygame.transform.rotate(pygame.transform.scale(self.image, (460*2, 400*2)), 90)
        #self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect(WIDTH / 2 - 600 ,HEIGHT / 2 - 460, 800, 920)
    def draw(self):
        #WIN.blit(self.image, ((WIDTH / 2) - 600 ,(HEIGHT / 2) - 460))
        pygame.draw.rect(WIN, BLACK, self.rect)

class ForegroundThingy():

    def __init__(self, background):
        self.foregroundlist = []
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x, background.rect.y - 20, 800, 20))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x - 20, background.rect.y, 20, 960))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x + 800, background.rect.y, 20, 960))
        self.foregroundlist.append(pygame.rect.Rect(background.rect.x, background.rect.y + 920, 800, 20))
        
    def draw(self):
        for i in self.foregroundlist:
            pygame.draw.rect(WIN, BLUE, i)

class Player:


    def __init__(self):
        self.rect = pygame.Rect(450, 100, 30, 30 )
        self.pos = self.rect.center
        self.hitbox = pygame.Rect(*(self.pos), 10, 10)
    


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
       # pygame.draw.rect(WIN, RED, self.hitbox)

    def bullet_handling(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_z]:
            if (pygame.time.get_ticks() - self.start_time) >= FIRERATE:
                self.start_time = pygame.time.get_ticks() 
                playerbullets.append(PlayerBullet(self.rect.centerx-10, self.rect.y))
                playerbullets.append(PlayerBullet(self.rect.centerx+10, self.rect.y)) 
               
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
    def __init__(self, x, y, player):
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
        self.speed = 7
    def update(self): 

        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        self.bullethbox.center = self.pos

        bulletrect = self.rotated_bullet.get_rect(center = self.bullethbox.center)

        surf.blit(self.rotated_bullet, bulletrect)
        #pygame.draw.rect(surf, RED, self.bullethbox)

class Bullet_H():
    def __init__(self, x, y, angle):
        self.bullethbox = pygame.Rect(x, y, 5, 5 )
        self.pos = (x, y)
        self.angle = angle
        self.bullet = pygame.image.load(os.path.join('bullethell', 'images', 'Sprites' , 'bigBullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (16, 16))
        self.speed = 7
    def update(self): 
        self.pos = calculate_angle(self.pos, self.speed, -self.angle)
        self.rect.center = round(self.pos[0]), round(self.pos[1])

    def draw(self, surf):
        self.bullethbox.center = self.pos

        bulletrect = self.rotated_bullet.get_rect(center = self.bullethbox.center)

        surf.blit(self.rotated_bullet, bulletrect)
        #pygame.draw.rect(surf, RED, self.bullethbox)

class Enemy():
    def __init__(self, x, y, player, xvel=0, yvel=0, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.pos = self.rect.center
        self.start_time = 0
        self.hp = 20
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
            if (pygame.time.get_ticks() - self.start_time) >= E_FIRERATE:
                self.start_time = pygame.time.get_ticks() 
                bullets.append(Bullet(*(self.pos), self.player))
        
    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (self.pos), 20)

class Enemy_2():
    def __init__(self, x, y, player, moveTime, xvel=0, yvel=0, isShooting=False):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.moveTime = moveTime*1000
        self.pos = self.rect.center
        self.start_time = 0
        self.start_time2 = 0
        self.clock = pygame.time.Clock()
        self.hp = 20
        self.player = player
        self.xvel = xvel
        self.yvel = yvel
        self.isShooting = isShooting
        run = True
    
        
    def update(self):
        time_delta = self.clock.tick(FPS)
        self.start_time2 += time_delta
        if self.start_time2 < self.moveTime:
            self.pos = self.rect.center
            self.rect.x += self.xvel
            self.rect.y += self.yvel
            if self.isShooting == True:
                if (pygame.time.get_ticks() - self.start_time) >= E_FIRERATE:
                    self.start_time = pygame.time.get_ticks() 
                    bullets.append(Bullet(*(self.pos), self.player))
        print(self.start_time2)


        
        
    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (self.pos), 20)


def calculate_angle(startxy, speed, angle):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle))
    return startxy + move_vec

def main():
    global clock
    clock = pygame.time.Clock()
    titleScreen(WIN)


def titleScreen(WIN):
    newGame = pygame.image.load("bullethell/images/BG+UI/new_game_button.jpg")


    closeGame = pygame.image.load("bullethell/images/BG+UI/exit_button.jpg")

    testSurf = pygame.surface.Surface((200,200))
    testSurf.fill(WHITE)
    buttons = [newGame,closeGame]
    loopContinues = True
    selected = buttons[0]
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
                    elif selected != buttons[1]:
                        #if you press up and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                if event.key == pygame.K_DOWN:
                    if selected != buttons[1]:
                        #if you press down and aren't on closeGame, that means you're on newGame. This moves you back to closeGame.
                        selected = buttons[1]
                    elif selected != buttons[0]:
                        #if you press down and aren't on newGame, that means you're on closeGame. This moves you back to newGame.
                        selected = buttons[0]
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
        WIN.blit(closeGame, (640,540))
        WIN.blit(newGame, (640,200))
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.update()
                        

class GameController():

    def __init__(self, background, player):
        self.now = 0
        self.passedTime = 0
        self.bounds = background.rect
        self.player = player
        self.clock = pygame.time.Clock()
    def update(self):
        time_delta = self.clock.tick(FPS)
        self.passedTime += time_delta

        randomx = random.randint(self.bounds.x + 100, 700)
        if self.passedTime < 10000:
            if (pygame.time.get_ticks() - self.now) >= 2000:
                self.now = pygame.time.get_ticks()
                if len(enemies) <= 5:
                    enemies.append(Enemy(randomx, 0, self.player, 0, 2, True))
            
        else:
            if (pygame.time.get_ticks() - self.now) >= 2000:
                self.now = pygame.time.get_ticks()
                enemies.append(Enemy_2(self.bounds.x + 400, 0, self.player, 1, 0, 2,))



                        
def pause(WIN):
    pass
    #fill this in later. The idea is to dim the screen (but not completely blacken it), quiet (but not mute) the music, and bring up the menu. Use EoSD as a reference
            
def gameOver(WIN):
    pass
#this should darken the screen, bring up a game over message, and then reuse a chunk of code from titleScreen() to give the player the option to go to the main menu or close the game.



                        
def gameLoop():
    run = True
    player = Player()
    background = Background()
    controller = GameController(background, player)
    foreground = ForegroundThingy(background)
    global timern
    timern = pygame.time.get_ticks()
    #enemies.append(Enemy_2(background.rect.x + 400, 0, player, 1, 0, 2,))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




        WIN.fill(BLUE)
        background.draw()



        controller.update()



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

        for enemy in enemies[:]:
            enemy.draw(WIN)
            enemy.update()
            if enemy.hp <= 0:
                enemies.remove(enemy)
            elif enemy.rect.y > HEIGHT:
                enemies.remove(enemy)

        foreground.draw()
        player.movement_handling(background)
        player.bullet_handling()
        player.draw()
        SCREEN.blit(pygame.transform.scale(WIN, SCREEN.get_rect().size), (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

    
#this should load all the sfx necessary for the game, initialize the player sprite (and set up the hitbox), set up the controls, make the shooting work, and then call a function to load level 1. We should make each level a separate module for convenience rather than keeping them all in 1 file imo                        
                        
main()
