from Utils import Graphics
from Objects import Entity
from Objects import StaticObject
import pygame
import sys
import random
#import threading

class Game():
    def __init__(self):
        pygame.init()
        self.resolution = (1080,720)
        self.window = pygame.display.set_mode(self.resolution)
        self.render_window = pygame.Surface((480,320))
        self.Render = Graphics.Render(self.render_window)
        self.player_lives = 3
        self.score = 0
        self.current_time = 0
        self.end_time = 360
        self.pause = 0
        self.SourcePoints = []
        pygame.display.set_caption("Nothing Frogger")
        self.static = []
        self.input = (0,0)
        for i in range(31):
            self.static.append(StaticObject.Trotuar(coordinates=(480-16*i,304)))
            self.static.append(StaticObject.Trotuar(coordinates=(480-16*i,240)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,224)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,208)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,192)))
            self.static.append(StaticObject.Trotuar(coordinates=(480-16*i,176)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,160)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,144)))
            self.static.append(StaticObject.Water(coordinates=(480-16*i,128)))
            self.static.append(StaticObject.Grass(coordinates=(480-16*i,98)))
            self.static.append(StaticObject.Grass(coordinates=(480-16*i,82)))
        for i in range(16):
            self.static.append(StaticObject.Grass(coordinates=(480-32*i,112)))
            self.SourcePoints.append(Entity.SourcePoint(coordinates=(480-32*i-16,112)))

        self.line1 =Entity.Spawner(Entity.Car,(480,288),-1,0,180)
        self.line2 =Entity.Spawner(Entity.Car,(0,272),1,1,200)
        self.line3 =Entity.Spawner(Entity.Car,(480,256),-1,0,220)
        self.line5 =Entity.Spawner(Entity.Tree,(0,224),1,1,150)
        self.line6 =Entity.Spawner(Entity.Turtle,(480,208),-1,1,180)
        self.line7 =Entity.Spawner(Entity.Tree,(0,192),1,1,190)
        self.line8 =Entity.Spawner(Entity.Turtle,(0,160),1,1,150)
        self.line9 =Entity.Spawner(Entity.Tree,(480,144),-1,1,180)
        self.line10 =Entity.Spawner(Entity.Turtle,(0,128),1,1,190)
        

        self.framerate = pygame.time.Clock()
        self.cars = []
        self.trees = []
        self.turtles = []
        self.player = Entity.player((240,304),"Player",self.render_window)
        self.FixedDeltaTime = 0

        #self.FixedTread = threading.Thread(target=self.FixedUpdate)
        #self.BackgroundTread = threading.Thread(target=self.Update)

    def User_Input(self,event = -1):
        input = (0,0)
        if event != -1:
            match event.type:
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_w | pygame.K_UP:
                                input = (0,-1)      
                            case pygame.K_s | pygame.K_DOWN:
                                input = (0,1)
                            case pygame.K_d | pygame.K_RIGHT:
                                input =  (1,0)
                            case pygame.K_a | pygame.K_LEFT:
                                input =  (-1,0)
                            case pygame.K_SPACE | pygame.K_KP_ENTER:
                                input = (-1,-1)
                            case pygame.K_ESCAPE:
                                input = (1,1)
                            case _:
                                input = (0,0)
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        else:
            for mevent in pygame.event.get():
                match mevent.type:
                    case pygame.KEYDOWN:
                        match mevent.key:
                            case pygame.K_w | pygame.K_UP:
                                input = (0,-1)      
                            case pygame.K_s | pygame.K_DOWN:
                                input = (0,1)
                            case pygame.K_d | pygame.K_RIGHT:
                                input =  (1,0)
                            case pygame.K_a | pygame.K_LEFT:
                                input =  (-1,0)
                            case pygame.K_SPACE | pygame.K_KP_ENTER:
                                input = (-1,-1)
                            case pygame.K_ESCAPE:
                                input = (1,1)
                            case _:
                                input = (0,0)
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        return input

    def MainMenu(self):
        pygame.mixer.music.load("Assets/Sounds/AFT - Initiation.mp3")
        pygame.mixer.music.play(-1)
        Label = Graphics.Button(coordinates=(110,10),content="Menu", fontsize=24)
        StartButton = Graphics.Button(content="1. Start",fontsize=14)
        WarningMessage = Graphics.Button(coordinates=(240,200),is_active=1,content="",fontsize=16,panel=self.render_window)
        SettingsButton = Graphics.Button(content="2. Settings",fontsize=14)
        ExitButton =Graphics.Button(content="3. Exit",fontsize=14)
        MenuStack = Graphics.StackPanel(coordinates=(10,30),size=(250,200),padding=30 ,content=[StartButton,SettingsButton,ExitButton],is_active=1)
        Panel = Graphics.Panel(coordinates=(40,40),size=(300,250), content=[Label,MenuStack],panel=self.render_window)
        while True:
            input = self.User_Input()
            if input ==(0,-1):
                MenuStack.index-=1
            if input==(0,1):
                MenuStack.index+=1
            if input ==(-1,-1):
                match MenuStack.index:
                    case 0:
                        self.FixedUpdate()
                        pygame.mixer.music.stop()
                    case 1:       
                        WarningMessage.content="Denied!!!"
                        WarningMessage.Render()
                        pygame.mixer.music.stop()
                    case 2:
                        pygame.quit()
                        sys.exit()    
            Panel.Render()
            WarningMessage.Render()
            self.window.blit(pygame.transform.scale(self.render_window, self.resolution),(0,0))
            pygame.display.update()
    
    def InfoBox(self):
        ScoreLabel = Graphics.Button(content=f"Score: {self.score}",fontsize=18)
        LivesLabel = Graphics.Button(content=f"Lives: {self.player_lives}", fontsize=18)
        Endbar = Graphics.ProgressBar(coordinates=(5,70),end=self.end_time,current=self.current_time,size=(470,5))
        stackpanel = Graphics.StackPanel(padding=200,orientation=0, content=[ScoreLabel,LivesLabel],size=(480,80),coordinates=(0,20))
        panel = Graphics.Panel(size=(480,85),content=[stackpanel,Endbar], panel=self.render_window)
        panel.Render()
    def PauseMenu(self):
        pygame.mixer.music.stop()
        Label = Graphics.Button(coordinates=(110,10),content="Pause", fontsize=24)
        StartButton = Graphics.Button(content="1. Start",fontsize=14)
        ExitButton =Graphics.Button(content="3. Exit",fontsize=14)
        MenuStack = Graphics.StackPanel(coordinates=(10,30),size=(250,200),padding=30 ,content=[StartButton,ExitButton],is_active=1)
        Panel = Graphics.Panel(coordinates=(40,40),size=(300,250), content=[Label,MenuStack],panel=self.render_window)
        while True:
            input = self.User_Input()
            if input ==(0,-1):
                MenuStack.index-=1
            if input==(0,1):
                MenuStack.index+=1
            if input ==(-1,-1):
                match MenuStack.index:
                    case 0:
                        self.pause = 0
                        self.FixedUpdate()
                    case 1:
                        pygame.quit()
                        sys.exit()    
            Panel.Render()
            self.window.blit(pygame.transform.scale(self.render_window, self.resolution),(0,0))
            pygame.display.update()

    def FindDeath(self):
        if self.player.is_alive == 0:
            self.player_lives -=1
            self.player.coordinates = [240,304] 
            self.player.is_alive = 1
        if self.player_lives<1 or self.end_time == self.current_time:
            while True:
                Label = Graphics.Button(coordinates=(10,60),fontsize=18,is_active=1,content=f"Game over!")
                Message = Graphics.Panel(size=(150,150),panel=self.render_window, coordinates=(180,100),content=[Label])
                Message.Render()
                self.window.blit(pygame.transform.scale(self.render_window, self.resolution),(0,0))
                pygame.display.update()
                self.cars.clear()
                self.trees.clear()
                self.turtles.clear()
                self.player_lives = 3
                self.current_time = 0
                self.score = 0
                for i in self.SourcePoints:
                    i.is_full = 0
                if self.User_Input() == (-1,-1):
                    self.MainMenu()
    def WinMessage(self):
        count = 0
        for i in self.SourcePoints:
            count+=i.is_full
        if len(self.SourcePoints)==count:
            while True:
                Label = Graphics.Button(coordinates=(10,60),fontsize=18,is_active=1,content=f"You win!!!")
                Message = Graphics.Panel(size=(150,150),panel=self.render_window, coordinates=(180,100),content=[Label])
                Message.Render()
                self.window.blit(pygame.transform.scale(self.render_window, self.resolution),(0,0))
                pygame.display.update()
                self.cars.clear()
                self.trees.clear()
                self.turtles.clear()
                self.player_lives = 3
                self.current_time = 0
                self.score = 0
                for i in self.SourcePoints:
                    i.is_full = 0
                if self.User_Input() == (-1,-1):
                    self.MainMenu()
    
    def FixedUpdate(self):
        tick = 0
        pygame.mixer.music.load("Assets/Sounds/Jeromy Cotton - Things Gonna Be a Lot Different Around Here.mp3")
        pygame.mixer.music.play(-1)
        while True:

            tick+=1
            if ((tick/60)%1==0):
                self.current_time += 1
                self.score+=1

            self.cars += self.line1.return_entityes()
            self.cars += self.line2.return_entityes()
            self.cars += self.line3.return_entityes()
            self.trees+= self.line5.return_entityes()
            self.trees+= self.line6.return_entityes()
            self.trees+= self.line7.return_entityes()
            self.turtles+=self.line8.return_entityes()
            self.turtles+=self.line9.return_entityes()
            self.turtles+=self.line10.return_entityes()
            self.render_window.fill((100,100,100))
            self.FixedDeltaTime = self.framerate.tick(60)/1000
            for static in self.static:
                static.Render(self.render_window)
            for car in self.cars:
                car.Update(self.player,self.FixedDeltaTime,self.render_window)
            for tree in self.trees:
                tree.Update(self.player,self.FixedDeltaTime,self.render_window)
            for turtle in self.turtles:
                turtle.Update(self.player,self.FixedDeltaTime,self.render_window)
            for EntryPoint in self.SourcePoints:
                EntryPoint.Update(self.player,self.render_window)
            self.InfoBox()
            self.FindDeath()
            self.input = self.User_Input()
            if self.input == (1,1):
                self.PauseMenu()
            self.player.Update(self.input,self.FixedDeltaTime,self.render_window,static_objects=self.static) 
            
            if self.pause:
                self.PauseMenu()
            self.window.blit(pygame.transform.scale(self.render_window, self.resolution),(0,0))
            pygame.display.update()
            

Game().MainMenu()                