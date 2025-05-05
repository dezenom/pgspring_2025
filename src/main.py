import pygame
import utils.ut as ut
import app as pp


app = pp.App()
rect = app.window.get_rect()

def desc():
    text = ut.ts.TextRenderer(30)
    while app.running:
        app.events()
        app.window.fill((10,30,30))
        text.render_text(app.window,"press esc to leave",(30,30),topleft =True)
        if ut.inputs.checkKeyPress("quit"):
            break


        text.render_text(app.window,"LMB - picking objects",(80,70),topleft =True)
        text.render_text(app.window,"RMB - dropping objects",(80,100),topleft =True)
        text.render_text(app.window,"address is read from leftmost runecatch ",(80,130),topleft =True)
        text.render_text(app.window,"to rightmost runecatch",(80,150),topleft =True)

        pygame.draw.rect(app.window,(0,0,0),rect,20)
        pygame.display.flip()

def main():
    ut.inputs.addKeybind("play",pygame.K_RETURN)

    buttons = [ut.ts.Button((260,60),size = (120,40),color = (70,60,50),text = "play",shadow_range = 30),ut.ts.Button((260,130),size = (120,40),color = (70,60,50),text = "controls",shadow_range = 30),ut.ts.Button((260,200),size = (120,40),color = (70,60,50),text = "quit",shadow_range = 30),]

    do = {
        "play":app.start,"controls":desc,"quit":app.stop
    }

    while app.running:
        app.window.fill((10,30,30))
        app.events()
        if ut.inputs.checkKeyPress("play"):
            app.playing = True
        for button in buttons:
            button.clicking()
            button.render(app.window)

            if button.clicked:
                do[button.text]()

        app.run()

        pygame.draw.rect(app.window,(0,0,0),rect,20)
        pygame.display.flip()
    pygame.quit()


main()
