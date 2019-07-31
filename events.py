import pygame
from pygame.locals import *
from Primitives.vectors import Vector2
from constants import *

class EventManager(object):
    def __init__(self, controller):
        self.controller = controller
        self.snapToGrid = False
        self.directedGraph = True
        
    def update(self, mouseposition):
        dt = self.controller.clock.tick(30) / 1000.0
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[K_UP] or key_pressed[K_w]:
            if self.controller.player is not None:
                self.controller.player.moveForward(dt)
        elif key_pressed[K_DOWN] or key_pressed[K_s]:
            if self.controller.player is not None:
                self.controller.player.moveBackward(dt)
                
        if key_pressed[K_RIGHT]:
            if self.controller.player is not None:
                self.controller.player.rotateCW(dt)
        elif key_pressed[K_LEFT]:
            if self.controller.player is not None:
                self.controller.player.rotateCCW(dt)
                
        if key_pressed[K_a]:
            if self.controller.player is not None:
                self.controller.player.strafeLeft(dt)
        elif key_pressed[K_d]:
            if self.controller.player is not None:
                self.controller.player.strafeRight(dt)

                
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_t:
                    self.controller.stepThroughTree()
                if event.key == K_5:
                    self.controller.getTestSector()
                if event.key == K_p:
                    self.controller.createPlayer()
                if event.key == K_SPACE:
                    self.controller.mode3D = not self.controller.mode3D
                    
    def getMousePosition(self, position):
        '''Gets the mouse position where we need to place the vertex.  If we are snapping to the grid, then modify the position, otherwise just pass it right through'''
        if self.snapToGrid:
            x = round(float(position.x) / TILEWIDTH) * TILEWIDTH
            y = round(float(position.y) / TILEHEIGHT) * TILEHEIGHT
            position = Vector2(x, y)
        return position
