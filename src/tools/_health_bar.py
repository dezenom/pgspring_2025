import pygame
import entity

# to be worked on
class HealthBar():
    def __init__(self,color,entity=entity.entity,size = [int,int]):
        self.entity = entity
        self.color = color
        self.size = size
        self.flow_h = size[0]
    def draw(self,screen,pos = [int,int]):
        ratio = self.entity.health/self.entity.maxhealth
        rect1 = pygame.Rect(pos[0],pos[1],self.size[0]*ratio,self.size[1])
        self.flow = pygame.Rect(pos[0],pos[1],self.flow_h,self.size[1])

        if self.flow_h > rect1.w:
            self.flow_h -=1
        if self.flow_h < rect1.w:
            self.flow_h +=2


        pygame.draw.rect(screen,self.color,self.flow)
