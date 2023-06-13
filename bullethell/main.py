import pygame, random

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
                        
                        
def pause(WIN):
    #fill this in later. The idea is to dim the screen (but not completely blacken it), quiet (but not mute) the music, and bring up the menu. Use EoSD as a reference
            
def gameOver(WIN):
#this should darken the screen, bring up a game over message, and then reuse a chunk of code from titleScreen() to give the player the option to go to the main menu or close the game.
                        
def gameLoop(WIN):
#this should load all the sfx necessary for the game, initialize the player sprite (and set up the hitbox), set up the controls, make the shooting work, and then call a function to load level 1. We should make each level a separate module for convenience rather than keeping them all in 1 file imo                        
                        
main()
