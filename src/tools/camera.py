import pygame

from globals import SCREENDIMENSIONS
import umath

class camera():
    def __init__(self):
        self.scroll = [0,0]

        size = (SCREENDIMENSIONS[0]*2,SCREENDIMENSIONS[1]*2)
        self.camera_view = pygame.Surface(size,pygame.SRCALPHA)
        self.camera_view_rect = self.camera_view.get_rect(center = (SCREENDIMENSIONS[0]//2,SCREENDIMENSIONS[1]//2))
        self.size_vector = pygame.math.Vector2(size)
        self.offset = pygame.math.Vector2((size[0] -SCREENDIMENSIONS[0])/2,(size[1] - SCREENDIMENSIONS[1])/2)
        self.render_scale = 1

        self.focus_entity = None
        self.y_sort_entities = []

    def get_Scroll(self):
        pos = umath.getOffset(self.focus_entity.center,self.scroll)

        self.scroll[0]+= pos[0]-SCREENDIMENSIONS[0]/2
        self.scroll[1]+= pos[1]-SCREENDIMENSIONS[1]/2


    def render(self,screen):
        self.get_Scroll()

        scroll = self.scroll -self.offset
        self.camera_view.fill((120,180,180))

        for sprite in sorted(self.y_sort_entities,key=lambda sprite:int(sprite.rect.y)):
            sprite.render(self.camera_view,scroll)

        transformed_screen = pygame.transform.scale(self.camera_view,self.size_vector*self.render_scale)
        rect = transformed_screen.get_rect(center =(SCREENDIMENSIONS[0]//2,SCREENDIMENSIONS[1]//2))
        screen.blit(transformed_screen,rect)

