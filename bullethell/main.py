import pygame, sprites_module, random

WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("ProjeCturne")
pygame.display.set_icon(pygame.image.load(images/BG+UI/icon.png) #when an icon is added, name it icon.png and put it in the filepath referenced here 
def main():
    while titleScreen(screen):
        if not gameLoop(screen):
            break
    pygame.quit()
    #when game_intro ends without gameLoop being called, this closes the game

def titleScreen(screen):
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
            if event.type == pygame.QUIT:
                loopContinues = False
                return 0
             
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [start_button]:
                        #select sfx should play here
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [quit_button]:
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
     
        # clears the screen so that the level assets can be loaded
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)                        
                        
                        
def pause(screen):
    background = screen
    #fill this in later. The idea is to dim the screen (but not completely blacken it), quiet (but not mute) the music, and bring up the menu. Use EoSD as a reference
            
def gameOver(screen):
#this should darken the screen, bring up a game over message, and then reuse a chunk of code from titleScreen() to give the player the option to go to the main menu or close the game.
                        
def gameLoop(screen):
#this should load all the sfx necessary for the game, initialize the player sprite (and set up the hitbox), set up the controls, make the shooting work, and then call a function to load level 1. We should make each level a separate module for convenience rather than keeping them all in 1 file imo                        
                        
main()
