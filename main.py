import pygame
import random
import datetime
import time
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_q,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

road_width = 130
width  = 640
height = 400
init_pos = [320-road_width/4,height*3/4]


class Car:
    def __init__(self,pos,xvel,yvel):
        self.pos = pos
        self.xvel = xvel
        self.yvel = yvel
        self.r_allowed = True
        self.l_allowed = False
        self.car_width = 20
        self.car_length = 50

class Obstacle:
    def __init__(self,pos,yvel):
        self.pos = pos
        self.yvel = yvel


pygame.init()
gameWindow=pygame.display.set_mode((width,height))
pygame.display.set_caption("Car Game")
pygame.display.update()
car = Car([320-road_width/4,height*3/4],0,0)
fps = 30
left = width/2 - 1.5*road_width/4
right = width/2 + road_width/4 - 20


def gameLoop():
    def record(car_pos,nearest_obs,result):
        f = open('train.csv','a')
        f.write(f'{car_pos[0]},{car_pos[1]},{nearest_obs[0]},{nearest_obs[1]},{result}\n')
        f.close()


    def restart():
        gameLoop()

    obss = []
    def createObs(side):
        obss.append(Obstacle([side,0],2))

    clock = pygame.time.Clock()
    exit_game = False
    pygame.font.init() # you have to call this at the start, 
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    start = datetime.datetime.now()
    score = 0
    obs_spawn_int = 2
    def reward():
        score+=1
        print(score)

    while not exit_game:
         #Event Management
        
        # Environmnet Control
        if car.pos[1] <= 10 or car.pos[1] >= 350:
            car.yvel = 0
        if car.pos[0] < 320-road_width/4:
            car.xvel = 0
            car.l_allowed = False
            car.r_allowed = True
        elif car.pos[0] >= 320+road_width/4-10:
            car.xvel = 0
            car.r_allowed = False 
            car.l_allowed = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == KEYDOWN:
                if event.key == K_RIGHT and car.r_allowed:
                    car.xvel=5  
                if event.key == K_LEFT and car.l_allowed:
                    car.xvel=-5
                if event.key == K_ESCAPE:
                    exit_game = True

        #Graphics
        gameWindow.fill((255,255,255))
        
        end = datetime.datetime.now()
        delta = end - start
        if(delta.seconds >= obs_spawn_int):
            start = end
            side = random.choice([right,left])
            createObs(side)
        
            
        for obs in obss:
            if(obs.pos[1] > height):
                del(obss[obss.index(obs)])
            obs.pos[1]+=obs.yvel
            pygame.draw.rect(gameWindow,(255,0,0),[obs.pos[0],obs.pos[1],40,40])
            
            
        curr_car_pos = (int(car.pos[0]),int(car.pos[1]))
        color_at_car_pos = gameWindow.get_at(curr_car_pos)
        if( color_at_car_pos == (255,0,0,255)):
            record(curr_car_pos,obss[0].pos,0)
            restart()
        
        try: 
            if(car.pos[1] == obss[0].pos[1]):
                record(curr_car_pos,obss[0].pos,1)
                score+=1
        except:
            pass    

        
        pygame.draw.rect(gameWindow,(0,0,0),[320-road_width/2,0,5,height])
        pygame.draw.rect(gameWindow,(0,0,0),[320+road_width/2,0,5,height])
        pygame.draw.line(gameWindow, (0,0,0),(320,0),(320,height))
        pygame.draw.rect(gameWindow,(0,200,0),[car.pos[0],car.pos[1],car.car_width,car.car_length])
        screen_text=myfont.render(f'Score: {score}',True,(0,0,0))
        gameWindow.blit(screen_text,[20,20])
        car.pos[0]+=car.xvel
        car.pos[1]+=car.yvel
        pygame.display.update()

        clock.tick(fps)

gameLoop()
pygame.quit()
