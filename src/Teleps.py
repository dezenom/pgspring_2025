import utils.ut as ut
import pygame
from collections import deque
from random import sample,randint

# what would i need for this,
# a Node class coordinates
# way to interpret how the Nodes are arranged and set up teleporters
# check collision with Parcel and see if its the right Parcel,
# send and record points, increase spawn rate depending on average sent Parcel


# give Node a set coordinate

# teleporter interprator arranged like english writing system,
# teleporters max of 4 Node points for the interpretor,
# take Node string at Node point and add to district string, if collided Parcels district string is same, destroy Parcel

def generateDistrict(nodes)->str:
    size = len(nodes)
    types = []
    for node in nodes:
        types.append(node.id)

    samples = sample(types,len(types))
    district = ""

    scale = 4
    # print
    image = pygame.Surface((int((nodes[0].rect.w)/scale*len(nodes)),int((nodes[0].rect.h)/scale)))
    x = image.get_size()[0]/len(nodes)

    for i,samp in enumerate(samples):
        district += samp[0:1]

    district = district[0:randint(1,6)]

    for i,samp in enumerate(samples):
        for node in nodes:
            if node.id == samp and samp[0:1] == district[i:i+1]:
                image.blit(pygame.transform.scale_by(node.image,1/scale),(x*i,0))

    image.set_colorkey((0,0,0))

    return (district, image)

    # __slots__ = ("pos","image","clicked","path","direction","size")

particles = ut.pts.ParticleHandler()

class Pather:
    def __init__(self,pos:ut.umath.Vec2,image_source:str):
        self.image = pygame.image.load(image_source).convert_alpha()
        self.pos = pos
        self.rect = self.image.get_frect(topleft = (pos.x,pos.y))
        self.clicked = False

        self.path = deque()
        self.direction = ut.umath.Vec2()

        self.size = min(self.image.get_size()[0],self.image.get_size()[1])

    def update(self):
        mouse_pos = ut.inputs.getMousePos()
        if self.clicked and len(self.path) < 100:
            if (self.pos - mouse_pos).magnitude() > 10:
                self.path.append(mouse_pos)


        if len(self.path):
            self.direction = (self.path[0] - self.pos).normalize()
            self.pos += self.direction * 15
            if (self.path[0] - mouse_pos).magnitude() <= 10:
                self.path.popleft()

        if pygame.mouse.get_just_pressed()[0]:
            if (self.pos - mouse_pos).magnitude() < self.size:
                self.clicked = True
        if pygame.mouse.get_just_pressed()[2]:
            self.clicked = False

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def render(self,surface):
        surface.blit(self.image,self.rect)

class Node(Pather):
    __slots__ = ("id","pos","rect","image","clicked","path","direction","size")
    def __init__(self,pos:ut.umath.Vec2,image_source:str,id:str = "none"):
        super().__init__(pos,image_source)
        self.id = id

class Parcel(Pather):
    __slots__ = ("district","districtimg","distimgrect","life","spawntime","inner","color","points","pos","rect","image","clicked","path","direction","size")
    def __init__(self,pos:ut.umath.Vec2,image_source:str,district:str = "none",life:int = 1800,points:int = 30):
        super().__init__(pos,image_source)
        self.district = district[0]
        self.districtimg = district[1]
        self.distimgrect = self.districtimg.get_bounding_rect()
        self.spawntime = 120

        self.life = life
        self.inner = 0
        self.color = (randint(0,255),randint(100,255),randint(50,255))
        self.points = points

        # self.text = ut.ts.TextRenderer(20)
    def render(self,surface):
        if self.spawntime <= 0:
            super().render(surface)
            # self.text.render_text(surface,self.district,self.rect.center,(200,200,200))
            pygame.draw.circle(surface,self.color,(self.rect.centerx,self.rect.top - 20),(1800 * self.life/1800)/100)
            pygame.draw.circle(surface,(255,100,100),(self.rect.centerx,self.rect.top - 20),(60 * self.inner/60)/10)
            surface.blit(self.districtimg,self.distimgrect)

    def update(self):
        if self.spawntime <= 0:
            super().update()
            self.life -= 1
            self.inner = self.inner + 1 if self.inner < 100 else 0
            self.distimgrect.center = (self.rect.centerx,self.rect.bottom + 10)
        else:
            self.spawntime -= 1
            particles.addParticle("shrink",particles.pt["shrink"]([self.rect.x,self.rect.y],radius = 5,color = self.color,direction = (randint(-100,100)/100,randint(-100,100)/100),glow = 1))

# Parcel wave maker
# generate Parcels at const range(random following the range), decrease the value of the max and min of the ranges with relation to amount of points the player has
class WavePlay():
    def __init__(self,main,init_timer = 300,prange = 100,wave_limit= 2,
                origin = ut.umath.Vec2(ut.globals.SCREENDIMENSIONS[0]/2,ut.globals.SCREENDIMENSIONS[1]/2+50)):
        self.main = main
        self.init_timer = init_timer
        self.timer = init_timer
        self.range = prange

        self.wave_limit = wave_limit
        self.wave = 0

        self.total_spawned = 0
        self.parcels = []
        self.images = ut.getFiles("res/images/parcels")
        self.origin = origin

        self.waiting = False


        self.text = ut.ts.TextRenderer(35)

    def controlParcels(self):
        if self.timer <= 0 and self.total_spawned < self.wave_limit:
            self.parcels.append(Parcel(self.origin + ut.umath.Vec2(randint(-self.range,self.range),randint(-self.range +50,self.range-50)),
                                        self.images[randint(0,len(self.images)-1)],
                                        generateDistrict(self.main.nodes),life = randint(1500+ 70 * self.wave_limit,1800+80 * self.wave_limit)) )
            self.main.pathers.append(self.parcels[-1])
            self.total_spawned +=1
            self.timer = self.init_timer
        if self.total_spawned >= self.wave_limit and not self.waiting:
            self.timer = 1800 + 60*self.wave_limit
            self.waiting = True
        if self.timer <= 0 and self.waiting:
            self.main.life -= len(self.parcels) * 2
            self.Parcels = []
            self.timer = self.init_timer
            self.waiting = False
            self.total_spawned = 0
            self.wave_limit += randint(0,2)


        if ut.inputs.checkKeyPress("skip") and self.waiting and len(self.parcels) == 0:
            self.timer = 0

        self.timer -= 1

        for i,parcel in enumerate(self.parcels):
            parcel.update()
            if parcel.rect.colliderect(self.main.teleporter.portal):
                if parcel.district == self.main.teleporter.district:
                    self.main.points += parcel.points * parcel.life/50
                    print(parcel.points * parcel.life/50)
                    self.parcels.pop(i)
                    self.main.active = False
            if parcel.life <=0:
                self.parcels.pop(i)
                self.main.life -= 5


    def render(self,surface):
        for parcel in self.parcels:
            parcel.render(surface)

        self.text.render_text(surface,str(int(self.timer/60+1)),(ut.globals.SCREENDIMENSIONS[0]/2,40),color = (200,200,200))

    def update(self):
        self.controlParcels()


# [50, 158, 374, 590, 698, 590]
class Teleporter:
    def __init__(self,main):
        self.rects = [
            pygame.Rect(70,240,32,32),
            pygame.Rect(90,110,32,32),
            pygame.Rect(230,60,32,32),
            pygame.Rect(380,60,32,32),
            pygame.Rect(510,110,32,32),
            pygame.Rect(530,240,32,32)
        ]
        self.background = pygame.image.load("res/images/background.png").convert_alpha()

        self.portal = pygame.Rect(0,0,48,64)
        self.portal.center = (ut.globals.SCREENDIMENSIONS[0]/2,ut.globals.SCREENDIMENSIONS[1]/2)

        self.container = ["","","","","",""]
        self.district = ""
        self.main = main

        self.colors = [(30,30,25),(25,40,40)]

        # self.text = ut.ts.TextRenderer()

    def render(self,surface):
        surface.blit(self.background,(0,0))
        surface.fill((60,80,80),special_flags = pygame.BLEND_RGB_MULT)

        particles.render(surface)

    def update(self):
        self.container = ["","","","","",""]
        self.district = ""
        for node in self.main.nodes:
            for i,rect in enumerate(self.rects):
                if node.rect.colliderect(rect):
                    self.container[i] = node.id
        for i in self.container:
            self.district += i[0:1]


        for i,rect in enumerate(self.rects):
            particles.addParticle("shrink",particles.pt["shrink"]([rect.centerx,rect.centery],radius = 2,color = self.colors[randint(0,1)],direction = (randint(-100,100)/100,randint(-100,100)/100),glow = 1))
        for parcel in self.main.wave_controller.parcels:
            if parcel.district == self.district:
                    particles.addParticle("shrink",particles.pt["shrink"]([self.portal.centerx,self.portal.centery],radius = 5,color = (100,100,100),direction = (randint(-100,100)/100,randint(-100,100)/100),glow = 1))

        particles.update()
