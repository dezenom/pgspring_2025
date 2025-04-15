import pygame,sys
import threading
from time import sleep

sys.path.append("tools")
pygame.init()

import inputs
import umath
import globals

maxspeed = 5
speed = [0,0]
acceleration = 0.4
friction = 0.5

################# startup for projects #####################

class app():
    def __init__(self,screen_dimensions=globals.SCREENDIMENSIONS):
        self.window = pygame.display.set_mode(screen_dimensions,flags=pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True
        self.change_scene = False
        self.rect = pygame.FRect(320,160,8,8)

        self.load = pygame.Surface((32,32))
        self.load.fill("red")
        self.load.set_colorkey((0,0,0))
        self.angle = 0


        inputs.addKeybind("up",pygame.K_w)
        inputs.addKeybind("down",pygame.K_s)
        inputs.addKeybind("left",pygame.K_a)
        inputs.addKeybind("right",pygame.K_d)
        inputs.addKeybind("quit",pygame.K_ESCAPE)



    def render(self):
        if not self.change_scene:
            self.window.fill("cyan")
            pygame.draw.rect(self.window,"red",self.rect,2)
        else:
            self.angle+=1
            image = pygame.transform.rotate(self.load,self.angle)
            self.window.fill((50,50,46))
            self.window.blit(image,(320-16,160-16))
        pygame.display.flip()

    def update(self):
        while True:
            global maxspeed,speed,acceleration,friction

            direction = inputs.getDirection("up","down","left","right")
            if direction[0]:
                speed[0] = umath.moveTowards(speed[0],acceleration,maxspeed*direction[0])
            else:speed[0] = umath.moveTowards(speed[0],friction,0)
            if direction[1]:
                speed[1] = umath.moveTowards(speed[1],acceleration,maxspeed*direction[1])
            else:speed[1] = umath.moveTowards(speed[1],friction,0)
            self.rect.x += speed[0]
            self.rect.y += speed[1]
            if inputs.checkKeyPress(pygame.K_q):
                self.change_scene = True
                self.rect.center = (320,160)
                sleep(2)
                self.change_scene = False

            if inputs.checkKeyPress("quit"):
                self.running = False
            self.clock.tick(60)


    def saveLoad(self):
        pass

    def run(self):
        update = threading.Thread(target=self.update,daemon=True)
        update.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    inputs.keyboard[str(event.key)] = True
                if event.type == pygame.KEYUP:
                    inputs.keyboard[str(event.key)] = False
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game=app()
    game.run()
