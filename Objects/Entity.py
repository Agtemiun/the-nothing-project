from random import randint
from turtle import speed
from types import coroutine
from xml.dom.minidom import Entity
import pygame
class CommonEntity():
    def __init__(self,coordinates,type):
        self.coordinates = list(coordinates)
        self.type = type
        self.image1 = pygame.image.load("Assets\\Tectures\\frogger\\frogg1.png")

        

    def get_rect(self):
        return pygame.Rect(self.coordinates[0],self.coordinates[1],16, 16)
    
    def get_center(self):
        return (self.coordinates[0]+8,self.coordinates[1]+8)

    def Update(self, movement):
        pass
    def Create(self, *args):
        pass

class player(CommonEntity):
    def __init__(self, coordinates, type, area):
        super().__init__(coordinates, type)
        self.is_alive = 1
        self.speed = 16
        self.on_boad = 1
        self.is_movement = 0
        self.area = area

    def get_objects_around(self,static_objects):
        around_objects = []
        for object in static_objects:
            if object.get_rect().collidepoint((self.get_center()[1],self.get_center()[1])):
                around_objects.append(object)
            if object.get_rect().collidepoint((self.get_center()[0]-16,self.get_center()[1])):
                around_objects.append(object)
            if object.get_rect().collidepoint((self.get_center()[0],self.get_center()[1]-16)):
                around_objects.append(object)
            if object.get_rect().collidepoint((self.get_center()[0]+16,self.get_center()[1])):
                around_objects.append(object)
            if object.get_rect().collidepoint((self.get_center()[0],self.get_center()[1]+16)):
                around_objects.append(object)
        return around_objects

    def Update(self,movement,delta,render_area, static_objects= []):
        objects_around = []
        
        if movement !=((0,0) or (-1,-1) or (1,1) or self.not_move != [0,0]):
            objects_around = self.get_objects_around(static_objects)
            self.is_movement = 1
            if 0<=self.coordinates[0]+movement[0]*self.speed<=self.area.get_size()[0] and 0<=self.coordinates[1]+movement[1]*self.speed<=self.area.get_size()[1]:
                
                for i in objects_around:
                    if i.get_rect().colliderect(pygame.Rect(self.coordinates[0]+16,self.coordinates[1],16,16)) and i.tag=="Grass" and movement[0]==1:
                        self.is_movement =0
                    if i.get_rect().colliderect(pygame.Rect(self.coordinates[0]-16,self.coordinates[1],16,16)) and i.tag=="Grass" and movement[0]==-1:
                        self.is_movement =0
                    if i.get_rect().colliderect(pygame.Rect(self.coordinates[0],self.coordinates[1]+16,16,16)) and i.tag=="Grass" and movement[1]==1:
                        self.is_movement =0
                    if i.get_rect().colliderect(pygame.Rect(self.coordinates[0],self.coordinates[1]-16,16,16)) and i.tag=="Grass" and movement[1]==-1:
                        self.is_movement =0
            if self.is_movement:
                self.coordinates[0] = self.coordinates[0]+self.speed*movement[0]
                self.coordinates[1] = self.coordinates[1]+self.speed*movement[1]

        render_area.blit(self.image1,self.coordinates)
        if self.on_boad == 0:
            for i in self.get_objects_around(static_objects):
                if i.get_rect().colliderect(self.get_rect()) and i.tag=="Water":
                    self.is_alive = 0 
        self.on_boad = 0
    
    def move(self,x,y):
        if 0<=self.coordinates[0]+x<=self.area.get_size()[0] and 0<=self.coordinates[1]+y<=self.area.get_size()[1]:
                self.coordinates[0] = self.coordinates[0]+x
                self.coordinates[1] = self.coordinates[1]+y

class Car(CommonEntity):
    def __init__(self,coordinates,speed = randint(70,120),is_left=1,variant = -1):
        super().__init__(coordinates,"car")
        self.is_left = is_left
        self.speed = speed
        self.imageOld = pygame.image.load("Assets\\Tectures\\big Car\\AnotherCar.png")
        self.image = pygame.image.load("Assets\\Tectures\\big Car\\car3.png")
        self.image1 = pygame.image.load("Assets\\Tectures\\big Car\\car2.png")
        self.image2 = pygame.image.load("Assets\\Tectures\\big Car\\car1.png")
        self.variants = [self.image,self.image1,self.image2]
        if variant == -1:
            self.current_image = self.imageOld
        else:
            self.current_image = self.variants[variant]

    
    def Car_hit(self,player):
        if self.get_rect().colliderect(player.get_rect()):
            player.is_alive = 0

    
    def Update(self,player,delta,render):
        self.Car_hit(player)
        if self.coordinates[0]>render.get_size()[0]+140 or self.coordinates[0]<-140:
            del self
            return

        self.coordinates[0] += self.is_left*self.speed*delta
        if self.is_left==-1:
            render.blit(pygame.transform.rotate(self.current_image,90),self.coordinates)
        else:
            render.blit(pygame.transform.rotate(self.current_image,270),self.coordinates)
    
    @staticmethod
    def Create(*args):
        return Car(args[0],args[1],args[2],args[4])

class Tree(CommonEntity):
    def __init__(self,coordinates,speed = randint(70,190),is_left=1,variant = 0):
        super().__init__(coordinates,"car")
        self.is_left = is_left
        self.speed = speed
        self.image = pygame.image.load("Assets\\Tectures\\Tree\\tree0.png")
        self.image1 = pygame.image.load("Assets\\Tectures\\Tree\\tree1.png")
        self.image2 = pygame.image.load("Assets\\Tectures\\Tree\\tree2.png")
        self.variants = [self.image,self.image1,self.image2]
        self.current_image = self.variants[variant]
        
    def on_tree(self,player,delta):
        if self.get_rect().collidepoint(player.get_center()):
            player.on_boad = 1
            player.move(self.is_left*self.speed*delta,0)
    
    def Update(self,player,delta,render):
        
        if self.get_center()[0]>render.get_size()[0]+140 or self.get_center()[0]<-140:
            del self
            return
        self.coordinates[0] += self.is_left*self.speed*delta
        self.on_tree(player,delta)
        if self.is_left==-1:
            render.blit(self.current_image,self.coordinates)
        else:
            render.blit(pygame.transform.rotate(self.current_image,180),self.coordinates)

    @staticmethod
    def Create(*args):
        return Tree(args[0],args[1],args[2],args[4])

class Turtle(CommonEntity):
    def __init__(self,coordinates,timer=randint(0,180),speed = randint(70,120),is_left=1):
        super().__init__(coordinates,"car")
        self.is_left = is_left
        self.underwater = 0
        self.timer = 0
        self.timing = timer
        self.speed = speed
        self.image = pygame.image.load("Assets\\Tectures\\Turtle\\Turtle1.png")
    
    def on_turtle(self,player,delta,render):
        if self.underwater == 0:
            if self.get_rect().collidepoint(player.get_center()):
                player.move(self.is_left*self.speed*delta,0)
                player.on_boad = 1
            if self.is_left==-1:
                render.blit(self.image,self.coordinates)
            else:
                render.blit(pygame.transform.rotate(self.image,180),self.coordinates)
            if (self.timer>self.timing-60):
                self.image = pygame.image.load("Assets\\Tectures\\Turtle\\Turtle2.png")
    
    def Update(self,player,delta,render):
        self.underwater = 0
        self.timer = (self.timer+1)%360
        if self.get_center()[0]>render.get_size()[0]+140 or self.get_center()[0]<-140:
            del self
            return
        
        
        if(self.timer>self.timing):
            self.underwater = 1      
        self.on_turtle(player,delta,render)
        if self.underwater==1:
            self.image = pygame.image.load("Assets\\Tectures\\Turtle\\Turtle3.png")
        self.coordinates[0] += self.is_left*self.speed*delta

    @staticmethod
    def Create(*args):
        return Turtle(args[0],args[3],args[1],args[2])    

class Spawner():
    def __init__(self,entity, coordinates, is_left, is_multiple, timing, diap = (3,9)):
        self.entity = entity
        self.coordinates = list(coordinates)
        self.is_left = is_left
        self.is_multiple = is_multiple
        self.timing = timing
        self.timer = 0
        self.diap =diap

    def return_entityes(self):
        entityes = []
        self.timer = (self.timer+1)%self.timing
        if(self.timer==0):
            rand1 = randint(80,100)
            rand2 = randint(330,350)
            end = randint(self.diap[0],self.diap[1])
            match self.is_multiple:
                    case 1:
                        for i in range(end):
                            if i == 0:
                                entityes.append(self.entity.Create((-116*self.is_left+self.coordinates[0]+i*16*self.is_left,self.coordinates[1]),rand1,self.is_left, rand2,0))
                            if i>0 and i<end-1:
                                entityes.append(self.entity.Create((-116*self.is_left+self.coordinates[0]+i*16*self.is_left,self.coordinates[1]),rand1,self.is_left, rand2,1))
                            if i == end-1:
                                entityes.append(self.entity.Create((-116*self.is_left+self.coordinates[0]+i*16*self.is_left,self.coordinates[1]),rand1,self.is_left, rand2,2))
                    case 0:
                        entityes.append(self.entity.Create(self.coordinates, rand1, self.is_left, rand2,-1))
        return entityes
        
class SourcePoint(CommonEntity):
    def __init__(self,coordinates):
        super().__init__(coordinates,type="EntryPoint")
        self.is_full = 0
    
    def Update(self, player,render):
        pygame.draw.rect(render,(140,140,140),self.get_rect())
        if self.is_full == 0:
            if self.get_rect().collidepoint(player.get_center()):
                self.is_full = 1
        else:
            pygame.draw.rect(render,(30,30,30),pygame.Rect(self.coordinates[0]+2,self.coordinates[1]+2,13,13))
        

        




             