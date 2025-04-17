import pygame,math
import umath
#### utils #####


# # parameters
#     image_source - file where the image is located
#     sprite_posx - position of the image to be gotten if the image is a sheet of sprites
#     size - size of a single sprite in the image if the image is a sheet of sprites
#     sprite_posy - y position if the sprite to be obtained if the image is a sheet of sprites

def get_image(image_source,sprite_posx=0,sprite_posy=0,size=(16,16))->pygame.Surface:
    fullimage = pygame.image.load(image_source)
    image = pygame.Surface((size[0],size[1]))
    lengthx = fullimage.get_width()/size[0] -1
    if sprite_posx > lengthx :
        sprite_posy += int(sprite_posx//lengthx)
        sprite_posx = int(sprite_posx%lengthx)-sprite_posy


    image.blit(fullimage,(sprite_posx*-size[0],sprite_posy*-size[1],size[0],size[1]))
    image.set_colorkey((0,0,0))

    return image

#image rotations, off exists due to differences in types of images created
def rotate_image(image,pos1,pos2,off = 90)->pygame.Surface:
    change = umath.change(pos1,pos2)
    hyp = umath.hyp(change)
    nvect = umath.normalizeVector(change,hyp) if hyp != 0 else (0.3,0)
    angle = math.degrees(math.atan2(change[1],change[0])) +off
    image.set_colorkey((0,0,0))
    return pygame.transform.rotate(image,-angle),nvect,-angle
def rotate_image_dir(image,dir,off = 90)->pygame.Surface:
    angle = math.degrees(math.atan2(dir[1],dir[0])) +off
    image.set_colorkey((0,0,0))
    return pygame.transform.rotate(image,-angle)

#text rendering , not a must to determine font
class TextRenderer:
    def __init__(self,size = 30,font = None):
        self.font = pygame.font.Font(font,size)

    def render_text(self,screen,text,pos=(16,16),color = (150,250,250),topleft = False):
        text = self.font.render(text,False,color)
        if not topleft:
            rect = text.get_rect(center = pos)
        else:
            rect = text.get_rect(topleft = pos)
        screen.blit(text,rect)

# # parameters
#     pos - position of the tile in world space
#     sprite_posx - position of the image to be gotten if the image is a sheet of sprites
#     tile_id - to differentiate tiles
#     image_source - file where the image is located
#     tile_size - size of a single tile
#     scale - how big the tile should be generated as at the start
class Tile:
    def __init__(self,pos,sprite_posx=None,tile_id = None,image_source=None,tile_size= (16,16),scale = 1):

        self.tile_id = tile_id

        if image_source != None:
            self.image = pygame.transform.scale_by(get_image(image_source,sprite_posx,size = tile_size),scale)
        else: 
            self.image = pygame.Surface((tile_size[0],tile_size[1]))
            self.image.fill((0,0,0))


        self.rect = self.image.get_frect(topleft=(pos[0],pos[1]))

    def render(self,screen,scroll):
        screen.blit(self.image,umath.getOffset(self.rect.topleft,scroll))





############################## button class , not integrated yet #################################
class Button:
    def __init__(self,pos,size = (54,45),color = (150,200,200),text = "Button",shadow_range = 100,text_size = 30):
        self.rect = pygame.FRect(pos[0],pos[1],size[0],size[1])
        self.color = color
        self.shadow_color = (color[0]-shadow_range,color[1]-shadow_range,color[2]-shadow_range)
        self.shadow_rect = self.rect.inflate(0,5)
        self.shadow_rect.y += size[1]/4
        self.text = text
        self.width = size[0]

        self.clicked = False
        self.button_text = TextRenderer(size = text_size)

    def clicking(self):
        self.clicked = False
        if pygame.mouse.get_just_pressed()[2] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.clicked = True

    def render(self,screen):
        self.clicking()
        self.shadow_rect.x = self.rect.x
        self.shadow_rect.y = self.rect.y + self.rect.h/4

        pygame.draw.rect(screen,self.shadow_color,self.shadow_rect)
        pygame.draw.rect(screen,self.color,self.rect)
        self.button_text.render_text(screen,self.text,self.rect.center)
