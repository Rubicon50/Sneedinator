import pygame,math,random

class Button(pygame.sprite.Sprite):
    #Button class, used in menus and stuff
    
    def __init__(self,xy_pos,message,color):
        pygame.sprite.Sprite.__init__(self)
        
        self.__message = message
        self.__font = pygame.font.Font(fonts/Comic Sans.ttf, 30)
        