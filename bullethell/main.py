import pygame, random, os



WIDTH, HEIGHT = 1280, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
GRAY = (255/2, 255/2, 255/2)
BLUE = (0, 0, 160)
VEL = 5
FIRERATE = 50
playerbullets = []

pygame.display.set_caption("ProjeCturne")
#pygame.display.set_icon(pygame.image.load('bullethell/images/BG+UI/icon.png')) #when an icon is added, name it icon.png and put it in the filepath referenced here 
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

class Player:


    def __init__(self):
        self.rect = pygame.Rect(450, 100, 30, 30 )
    


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
    def draw(self):
        pygame.draw.circle(WIN, YELLOW, self.rect.center, 15)

    def bullet_handling(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_z]:
            if (pygame.time.get_ticks() - self.start_time) >= FIRERATE:
                self.start_time = pygame.time.get_ticks() 
                playerbullets.append(PlayerBullet(self.rect.centerx-10, self.rect.y))
                playerbullets.append(PlayerBullet(self.rect.centerx+10, self.rect.y)) 
                print(playerbullets)
               
class PlayerBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-5, y-20, 5, 30)
        self.pos = self.rect.x, self.rect.y
        self.bullet = pygame.image.load(os.path.join('bullethell','images', 'BG+UI' , 'bullet.png'))
        self.bullet = pygame.transform.scale(self.bullet, (10, 40))
        self.destroy = False

    def update(self):
        self.rect.y -= 7
    def draw(self, surf):
        surf.blit(self.bullet, self.rect)


def main():
    global clock
    clock = pygame.time.Clock()
    gameLoop()

def titleScreen(WIN):
    #this function contains all the code for the main menu. Once a new game is started, main() will automatically continue.
    background = pygame.image.load(images/BG+UI/main_background.jpg)
    newGame = pygame.image.load(image/BG+UI/new_game_button.jpg)
    newGame.blit(320,230)
    closeGame = pygame.image.load(images/BG+UI/exit_button.jpg)
    closeGame.blit(320,270)
    pygame.display.update()
    buttons = [newGame,closeGame]
    #we should add a clock variable that's tied to the internal clock so that enemy spawns can be predetermined based on time, I'll add this later.
    #sfx and bgm that are used on the title screen should be loaded in this function too, make a variable that equals the sound. then just type "[sfx var. name].play()" when it needs to play
    loopContinues = True
    selected = [buttons[0]]
    while loopContinues:
        clock.tick(FPS)
        #Clock's ticking is now tied to the FPS
        
        #we do a little event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loopContinues = False
                return 0
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != ["start_button"]:
                        #select sfx should play here
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != ["quit_button"]:
                        #select sfx should play here
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                if event.key == pygame.K_z:
                        if selected == [newGame]:
                            #stop the music here as well since the 1st stage music will be loaded alongside stage 1
                            #Return start game loop value.
                            return 1
                        elif selected == [closeGame]:
                            #Return exit game value. 
                            return 0                       
                                    
        #this should make the button you're hovering over light up a bit
        for select in selected:
            select.set_select()                       
                        
                        
def pause(WIN):
    pass
    #fill this in later. The idea is to dim the screen (but not completely blacken it), quiet (but not mute) the music, and bring up the menu. Use EoSD as a reference
            
def gameOver(WIN):
    pass
#this should darken the screen, bring up a game over message, and then reuse a chunk of code from titleScreen() to give the player the option to go to the main menu or close the game.



                        
def gameLoop():
    foregroundThingy = pygame.rect.Rect(WIDTH / 2 - 600, HEIGHT / 2 - 480, 800, 20)
    run = True
    player = Player()
    background = Background()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()




        WIN.fill(BLUE)
        background.draw()

        for bullet in playerbullets:
            bullet.draw(WIN)
            bullet.update()
            if not bullet.rect.colliderect(background.rect):
                playerbullets.remove(bullet)
        
        player.movement_handling(background)
        player.bullet_handling()
        player.draw()
        pygame.draw.rect(WIN, BLUE, foregroundThingy)
        pygame.display.flip()
        clock.tick(FPS)

    
#this should load all the sfx necessary for the game, initialize the player sprite (and set up the hitbox), set up the controls, make the shooting work, and then call a function to load level 1. We should make each level a separate module for convenience rather than keeping them all in 1 file imo                        
                        
main()