import pygame
from pygame.locals import *
from Primitives.vectors import Vector2
from constants import *

class EventManager(object):
    def __init__(self, controller):
        self.controller = controller
        self.snapToGrid = False
        self.directedGraph = False
        
    def update(self, mouseposition):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_g:
                    #toggle the grid on and off
                    self.controller.showGrid = not self.controller.showGrid
                if event.key == K_1:
                    #Move the vertices around to different positions
                    self.controller.editMode = not self.controller.editMode
                    self.controller.connectionMode = False
                    self.controller.checkMode = False
                    self.controller.probeMode = False
                if event.key == K_2:
                    #connect undirected segments between vertices
                    self.controller.editMode = False
                    self.controller.checkMode = False
                    self.controller.probeMode = False
                    self.controller.connectionMode = not self.controller.connectionMode
                if event.key == K_3:
                    self.controller.editMode = False
                    self.controller.connectionMode = False
                    self.controller.probeMode = False
                    self.controller.checkMode = not self.controller.checkMode
                if event.key == K_s:
                    self.snapToGrid = not self.snapToGrid
                    print("snap to grid : " + str(self.snapToGrid))
                if event.key == K_x:
                    #Erase all the neighbors from all the vertices (don't erase the vertices though)
                    self.controller.removeNeighbors()
                if event.key == K_z:
                    #Erase everything from the screen and start from scratch
                    self.controller.setup()
                if event.key == K_d:
                    self.directedGraph = not self.directedGraph
                    print("Directed graph = " + str(self.directedGraph))
                if event.key == K_n:
                    self.controller.showVertices = not self.controller.showVertices
                if event.key == K_b:
                    self.controller.createBinaryTree()
                    
            if event.type == MOUSEBUTTONDOWN:
                if self.controller.editMode:
                    self.controller.followMouse = True
                elif self.controller.connectionMode:
                    if self.controller.hoverVertex is not None:
                        self.controller.createConnectionLine()
                elif self.controller.checkMode:
                    if self.controller.hoverVertex is not None:
                        self.controller.printVertexInfo()
                elif self.controller.probeMode:
                    self.controller.createProbe(mouseposition)
                    self.controller.followMouse = True
                else:
                    if self.controller.hoverVertex is None:
                        self.controller.createVertexShadow(mouseposition)

            if event.type == MOUSEBUTTONUP:
                if self.controller.editMode:
                    self.controller.followMouse = False
                    if self.controller.hoverVertex is not None:
                        self.controller.hoverVertex.position = self.getMousePosition(mouseposition)
                elif self.controller.connectionMode:
                    if self.controller.hoverVertex is not None:
                        if self.directedGraph:
                            self.controller.connectVerticesDirected()
                        else:
                            self.controller.connectVerticesUndirected()
                    self.controller.connectionLine = None
                    self.controller.vertex0 = None
                elif self.controller.probeMode:
                    self.controller.followMouse = False
                    self.controller.probe.position = self.getMousePosition(mouseposition)
                if self.controller.vertexShadow is not None:
                    position = self.getMousePosition(mouseposition)
                    self.controller.createVertex(position)
                else:
                    pass

    def getMousePosition(self, position):
        '''Gets the mouse position where we need to place the vertex.  If we are snapping to the grid, then modify the position, otherwise just pass it right through'''
        if self.snapToGrid:
            x = round(float(position.x) / TILEWIDTH) * TILEWIDTH
            y = round(float(position.y) / TILEHEIGHT) * TILEHEIGHT
            position = Vector2(x, y)
        return position
