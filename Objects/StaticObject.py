import re
import pygame
class StaticObject():
    def __init__(self,tag,image,coordinates):
        self.tag = tag
        self.image = image
        self.coordinates = coordinates
    
    def get_rect(self):
        return pygame.Rect(self.coordinates[0],self.coordinates[1],16,16)

class Water(StaticObject):
    def __init__(self,coordinates = (0,0)):
        super().__init__("Water",pygame.image.load("Assets\\Tectures\\Water\\water.png"),coordinates)
    
    def Render(self,render):
        render.blit(self.image,self.coordinates)

class Trotuar(StaticObject):
    def __init__(self,coordinates = (0,0)):
        super().__init__("Trotuar",pygame.image.load("Assets\\Tectures\\Trotuar\\trtuar.png"),coordinates)
    
    def Render(self,render):
        render.blit(self.image,self.coordinates)

class Grass(StaticObject):
    def __init__(self,coordinates = (0,0)):
        super().__init__("Grass",pygame.image.load("Assets\\Tectures\\Grass\\grass.png"),coordinates)
    
    def Render(self,render):
        render.blit(self.image,self.coordinates)