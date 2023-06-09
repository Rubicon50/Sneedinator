import pygame, sprites_module, random

WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("ProjeCturne [PLACEHOLDER]")
pygame.display.set_icon(pygame.image.load(images/BG+UI/icon.png) #when an icon is added, name it icon.png and put it in the filepath referenced here 
def main():
    while game_intro(screen):
        if not game_loop(screen):
            break
    pygame.quit()
    #when game_intro ends without gameLoop being called, this closes the game.



def pause(screen):
    background = screen
    #fill this in later. The idea is to dim the screen (but not completely blacken it), quiet (but not mute) the music, and bring up the menu. Use EoSD as a reference

def game_intro(screen):
    #this function contains all the code for the main menu. Once a new game is started, main() will automatically continue.
    background = #load title screen BG
    newGame = game_sprites.button #load image that will be used as new game button, make sure it has the right X/Y coords
    closeGame = game_sprites.button #load image that will be used as exit button, make sure it has the right X/Y coords
    #list of buttons to make event handling easier
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
            
