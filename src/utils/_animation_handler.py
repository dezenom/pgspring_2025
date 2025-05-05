import pygame
from utils._tile_support import get_image

class AnimationHandler():
    def __init__(self,animation_speed, SPRITESHEET, FRAMESIZE) :
        self.SPRITESHEET = SPRITESHEET
        # animation control
        self.animation_speed = animation_speed
        self.current_index = 0
        #framesize of one sprite in the spritesheet, used to move along the sprite sheet
        self.FRAMESIZE = FRAMESIZE

    def animation(self,status,flip=[False,False])->pygame.Surface:
        #increment to the index of the animation
        self.current_index+=self.animation_speed
        if self.current_index >= 11*5:
            self.current_index = 0
        
        #status as in the y position of the animation in the sprite sheet
        image = pygame.transform.flip(get_image(self.SPRITESHEET,self.current_index//5,size=self.FRAME_SIZE,layery=status),flip[0],flip[1])

        # check if the image box is empty if so restart the animation
        rect = image.get_bounding_rect()
        if rect.w == 0 and rect.h == 0:
            self.current_index = 0
            image = pygame.transform.flip(get_image(self.SPRITESHEET,self.current_index//5,size=self.FRAME_SIZE,layery=status),flip[0],flip[1])

        return image
    
