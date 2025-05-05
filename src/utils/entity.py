import pygame
import utils.umath as umath

## parameters
#   size - size of the entity,should never be changeable for now atleast
#   MOVEMENTDATA -[
#         MAGNITUDES = MOVEMENTDATA[0] #maxspeed
#         ACCELERATION = MOVEMENTDATA[1] #increment
#         FRICTION = MOVEMENTDATA[2] #decrement
#         GRAVITY = MOVEMENTDATA[3] #if need be
# ]

class entity:
    def __init__(self,size,MOVEMENTDATA=[(800,800),40,20,0.8,180]):

        self.image = pygame.Surface(size).convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_frect()

        self.animation_status = 0
        self.flip = [0,0]

        self.MAGNITUDES = MOVEMENTDATA[0]
        self.ACCELERATION = MOVEMENTDATA[1]
        self.FRICTION = MOVEMENTDATA[2]
        self.GRAVITY = MOVEMENTDATA[3]

        self.reducer = MOVEMENTDATA[4]

        self.vector = pygame.Vector2()

        self.health = 0
        self.MAXHEALTH = 0


    def render(self,screen,scroll=(0,0)):
        pos = umath.getOffset(self.rect.topleft,scroll)
        screen.blit(self.image,pos)
        rect = self.image.get_frect(topleft = pos)
        pygame.draw.rect(screen,(100,100,100),rect,2)
