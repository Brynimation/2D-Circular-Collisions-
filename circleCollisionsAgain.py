#Sources:

#imports
import pygame as pg
import pygame_gui as gui
import os
import time 
import random
from Ball import Ball
#setup
pg.init()
width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("balls")

manager = gui.UIManager((width, height))

run = True
clock = pg.time.Clock()
lMousePressed = False
rMousePressed = False
drawing = False 
coefficientOfFriction = 0.05




balls = []


addBallButton = gui.elements.UIButton(pg.Rect((0, 0), (50, 50)), text="+ball", manager=manager)
removeBallButton = gui.elements.UIButton(pg.Rect((0, 50), (50, 50)), text="-ball", manager = manager)
slider = gui.elements.UIHorizontalSlider(pg.Rect((275, 25), (200, 20)), start_value = 0.05, value_range=(0.00, 0.95), manager=manager)
font = pg.font.SysFont("Impact", 20)



for i in range(10):
     balls.append(Ball(random.randint(0, width), random.randint(0, height), (20 - i) , (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
velVector = pg.math.Vector2(0, 0)

while run:
    message = "Coefficient of friction: 0.0" + str(int(100 * coefficientOfFriction)) if coefficientOfFriction < 0.1 else "Coefficient of friction: 0." +  str(int(100 * coefficientOfFriction))
    text = font.render(message, False, (255, 255, 255))
    timeDelta = clock.tick()/1000 # time taken in seconds between loops
    mouseVector = pg.math.Vector2(int(pg.mouse.get_pos()[0]), int(pg.mouse.get_pos()[1]))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: #Left mouse button
                lMousePressed = True
            elif event.button == 3: #Right mouse button
                rMousePressed = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                lMousePressed = False
            elif event.button == 3:
                rMousePressed = False
        elif event.type == pg.USEREVENT:
            if event.user_type == gui.UI_BUTTON_PRESSED:
                if event.ui_element == addBallButton:
                    balls.append(Ball(random.randint(0, width), random.randint(0, height), (20 - i) , (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                elif event.ui_element == removeBallButton:
                    if len(balls) != 0:
                        balls.pop()
            if event.user_type == gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider:
                    coefficientOfFriction = slider.get_current_value()
        manager.process_events(event)
      
    manager.update(timeDelta)
    win.fill((0,0,0))
    for ball in  balls:
        ball.display(win)
        ball.staticCollision(balls, win)
        if lMousePressed and ball.collisionCheck(mouseVector, ball.radius):
            ball.selected = True
            ball.pos = mouseVector
        elif (rMousePressed and ball.collisionCheck(mouseVector, ball.radius)) or (rMousePressed and drawing and ball.selected):
            ball.selected = True
            drawing = True
        else:
            ball.selected = False
            ball.updatePos(ball.vel, width, height, coefficientOfFriction)
        
        if ball.selected:
            velVector = ball.pos - mouseVector
            ball.vel = velVector
            pg.draw.line(win, (0, 255, 0), ball.pos, mouseVector)
        if not rMousePressed:
            drawing = False

        #win.blit(borderImg, (0,0)) #blit draws an image to the surface, win
        win.blit(text, (275, 0))

        

    manager.draw_ui(win)
    clock.tick(30)
    pg.display.update()

