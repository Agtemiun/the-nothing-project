from ast import While
from time import sleep
import pygame
import random
class Render():
    def __init__(self,surface,*layers):
        self.count_layers = len(layers)
        self.layer = layers
        self.render_surface = surface

    def Test_render(self):
        self.render_surface.fill((random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        sleep(0.3)


class Button():
    def __init__(self,coordinates = (0,0), fontsize = 8, padding = 0, is_active = 0, panel = pygame.surface.Surface((100,20)),content = "Undefined Text"):
        self.coordinates = coordinates
        self.fontsize = fontsize
        pygame.init()
        self.font = pygame.font.Font('FFFFORWA.TTF',self.fontsize)
        self.padding = padding
        self.is_active = is_active
        self.panel = panel
        self.content = content
        self.size = self.font.render(content,False,self.fontsize).get_size()
        

    def Render(self):
        self.panel.blit(self.font.render(self.content,False,(91,110,255)),self.coordinates)
        if self.is_active == 1:
            self.panel.blit(self.font.render(self.content,False,(153,229,80)),self.coordinates)
        self.is_active=0
class Panel():

    def __init__(self,coordinates = (0,0),panel = pygame.surface.Surface((100,20)), size=(250,200), content = []):
        self.coordinates = coordinates
        self.panel = panel
        self.size = size
        self.surface = pygame.surface.Surface(self.size)
        
        self.content = content
        for i in self.content:
            i.panel = self.surface
        
    def Render(self):
        pygame.draw.rect(self.surface,(99,155,255),pygame.Rect(0,0,self.size[0],self.size[1]))
        pygame.draw.rect(self.surface,(91,110,255),pygame.Rect(0,0,self.size[0],self.size[1]),3)
        for i in self.content:
            i.Render()
        self.panel.blit(self.surface,self.coordinates)

class ProgressBar():

    def __init__(self,size=(100,5),coordinates=(0,0),end=100,current=0, panel= pygame.surface.Surface((100, 20))):
        self.size = size
        self.coordinates = coordinates
        self.end = end
        self.panel = panel
        self.current = current
        self.step = size[0]/self.end

    def Render(self):
        pygame.draw.rect(self.panel,(153,229,80),pygame.Rect(self.coordinates[0],self.coordinates[1],self.size[0],self.size[1]))
        pygame.draw.rect(self.panel,(91,110,255),pygame.Rect(self.coordinates[0],self.coordinates[1],(self.current*self.step)%self.size[0],self.size[1]))
        
class StackPanel(Panel):
    def __init__(self, coordinates=(0, 0), panel=pygame.surface.Surface((100, 20)), size=(250, 200),orientation = 1,content = [],padding=20, is_active = 0):
        super().__init__(coordinates, panel, size,content=content) 
        self.padding = padding
        self.orientation = orientation
        self.index = 0
        self.is_active = is_active
        self.surface.fill((0,0,0))
        self.surface.set_colorkey((0,0,0))

    def Render(self):
        for i in range(len(self.content)):
            if self.is_active:
                if self.index>len(self.content):
                    self.index = 0
                if self.index<0:
                    self.index = len(self.content)-1
                if i == self.index:
                    self.content[i].is_active=1
            if self.orientation == 1:
                self.content[i].coordinates = (0,self.coordinates[1]+self.content[i].size[1]+i*self.padding)
                self.content[i].Render()
            if self.orientation == 0:
                self.content[i].coordinates = (self.content[i].coordinates[0]+self.content[i].size[0]+i*self.padding,0)
                self.content[i].Render()
            self.panel.blit(self.surface,self.coordinates)