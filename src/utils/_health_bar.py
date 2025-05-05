import pygame

# to be worked on
class RatioBar():
    def __init__(self,color,max,size = [int,int]):
        self.max = max
        self.color = color
        self.size = size
        self.flow_h = size[0]
    def render(self,surface,current,pos = [int,int]):
        ratio = current/self.max
        rect1 = pygame.Rect(pos[0],pos[1],self.size[0]*ratio,self.size[1])
        self.flow = pygame.Rect(pos[0],pos[1],self.flow_h,self.size[1])

        if self.flow_h > rect1.w:
            self.flow_h -=1
        if self.flow_h < rect1.w:
            self.flow_h +=2


        pygame.draw.rect(surface,self.color,self.flow)
