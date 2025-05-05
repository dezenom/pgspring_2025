import pygame
from random import randint

############  SHRINK PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction
############  PULSE PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction, 5 = pulse_range, 6 = life
############  FALL PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction, 5 = fall_speed

#argurments ######     pos,[radius,color,direction,##for pulse##(pulse_range,life)#####,##for fall##(fall_speed)#####]      #######

class ParticleHandler:
    def __init__(self):

        self.setParticles()

    def setParticles(self):

        self.particle_speed = 1

        self.shrink_particles = []
        self.shrink_speed = 0.1
        self.all_particles = {"shrink":self.shrink_particles}

        self.setBuild()

    def setBuild(self):
        def shrinkParticle(pos,**kwargs):
            surf = pygame.Surface((kwargs["radius"]*2,kwargs["radius"]*2))
            pygame.draw.circle(surf,kwargs["color"],(kwargs["radius"],kwargs["radius"]),kwargs["radius"])
            surf.set_colorkey((0,0,0))

            if "glow" not in kwargs:
                surf = 0

            return [randint(kwargs["radius"],kwargs["radius"]+2),pos,kwargs["color"],surf,kwargs["direction"]]

        self.pt = {"shrink":shrinkParticle}

    def addParticle(self,type,particle):
        self.all_particles[type].append(particle)

    def update(self):
        for ind,particle in enumerate(self.shrink_particles):
            particle[0] -= self.shrink_speed
            particle[1][0] += self.particle_speed*particle[4][0]
            particle[1][1] += self.particle_speed*particle[4][1]
            if particle[0] <= 0:
                self.shrink_particles.pop(ind)

    def render(self,surface):
        for key in self.all_particles.keys():
            for particle in self.all_particles[key]:
                pygame.draw.circle(surface,particle[2],particle[1],particle[0])
                if particle[3]!=0:
                    surface.blit(particle[3],(particle[1][0]-particle[3].get_width()/2,particle[1][1]-particle[3].get_height()/2),special_flags =  pygame.BLEND_RGB_ADD)


############  SHRINK PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction
############  PULSE PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction, 5 = pulse_range, 6 = life
############  FALL PARTICLES CONTAINER : 0 = radius,1 = pos, 2 = color, 3 = glow surf, 4 = direction, 5 = fall_speed
