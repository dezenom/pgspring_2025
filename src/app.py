import pygame

pygame.init()

import utils.ut as ut
import Teleps

class App():
    def __init__(self,screen_dimensions=ut.globals.SCREENDIMENSIONS):
        self.window = pygame.display.set_mode(screen_dimensions,flags=pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.life = 50
        self.hbar = ut.bar.RatioBar((255,100,100),self.life,[120,16])
        self.points = 0

        self.text = ut.ts.TextRenderer(40)

        ut.inputs.addKeybind("quit",pygame.K_ESCAPE)
        ut.inputs.addKeybind("skip",pygame.K_SPACE)

        self.nodes = [
            Teleps.Node(ut.umath.Vec2(100,100),"res/images/nodes/circle.png","circle"),
            Teleps.Node(ut.umath.Vec2(200,100),"res/images/nodes/rectangle.png","rectangle"),
            Teleps.Node(ut.umath.Vec2(400,130),"res/images/nodes/square.png","square"),
            Teleps.Node(ut.umath.Vec2(500,100),"res/images/nodes/triangle.png","triangle"),
            Teleps.Node(ut.umath.Vec2(600,130),"res/images/nodes/light.png","light"),
            Teleps.Node(ut.umath.Vec2(300,100),"res/images/nodes/dark.png","dark")

        ]
        self.pathers = []
        self.pathers.extend(self.nodes)

        self.teleporter = Teleps.Teleporter(self)
        self.wave_controller = Teleps.WavePlay(self,60)

        self.active = False


    def render(self):
        self.window.fill((100,100,100))

        self.teleporter.render(self.window)
        for node in self.nodes:
            node.render(self.window)
        self.wave_controller.render(self.window)

        self.hbar.render(self.window,self.life,[10,15])
        self.text.render_text(self.window,str(int(self.points)),(ut.globals.SCREENDIMENSIONS[0] - 100,20),color = (200,200,200))
        self.text.render_text(self.window,"space to skip",(ut.globals.SCREENDIMENSIONS[0]/2,ut.globals.SCREENDIMENSIONS[1]-20),color = (200,200,200))

        pygame.display.flip()

    def update(self):
        self.wave_controller.update()

        if ut.inputs.checkKeyPress("quit"):
            self.playing = False
        for node in self.nodes:
            node.update()
        for obj in self.pathers:
            if self.active:
                obj.clicked = False
            if obj.clicked:
                self.active = True
        self.active = False

        self.teleporter.update()

        self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            if event.type == pygame.KEYDOWN:
                ut.inputs.keyboard[str(event.key)] = True
            if event.type == pygame.KEYUP:
                ut.inputs.keyboard[str(event.key)] = False

    def stop(self):
        self.running = False
        self.playing = False
    def start(self):
        self.playing = True

    # def saveLoad(self):
    #     pass

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.render()
            self.clock.tick(60)

            fps = self.clock.get_fps()
            pygame.display.set_caption(f"Your Game Title - FPS: {fps:.2f}")

