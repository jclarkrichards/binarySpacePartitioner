import pygame
from constants import *
#import utils
from math import floor
from Primitives.vectors import Vector2
from Primitives.vertex import Vertex, VertexShadow
from Primitives.lines import Line
from Primitives.segment import Segment
from events import EventManager
from bsp import BinarySpacePartitioner as BSP

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_edit = None
        self.background_connection = None
        self.background_check = None
        self.setBackground()
        self.grid = [] #list of lines that define the grid
        self.setup()
        self.events = EventManager(self)
        
    def setup(self):
        self.vertices = {}
        self.vertexShadow = None
        self.showVertices = True
        self.editMode = False #move vertices around
        self.connectionMode = False #connect vertices together
        self.checkMode = False #For checking the vertices properties by clicking on them
        self.probeMode = False #For testing.  Create a probe point (vertex)
        self.drawGraphQuickMode = False
        self.hoverVertex = None #vertex the mouse is hovering over at any point in time
        self.vertex0 = None #vertex that connection line is coming from
        self.followMouse = False #If true then the hoverVertex will follow the mouse if it is not None
        self.drawConnectionLine = False
        self.connectionLine = None #The line that shows when you are drawing a line from one vertex to the next
        self.showGrid = False
        self.vertex_key_ctr = 0
        self.bsp = None
        self.testvertexlist = []
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(DARKGRAY)
        self.background_edit = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_edit.fill(BACKGROUNDEDIT)
        self.background_connection = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_connection.fill(CONNECTIONMODECOLOR)
        self.background_check = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_check.fill(CHECKMODECOLOR)
        self.background_probe = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_probe.fill(PROBEMODECOLOR)
        self.segments = [] #make global for testing so we can see them dynamically
        
    def defineGrid(self):
        '''Defines vertical and horizontal lines'''
        #Define vertical lines
        for i in range(NCOLS):
            self.grid.append(Line(Vector2(i*TILEWIDTH, 0), Vector2(i*TILEWIDTH, SCREENHEIGHT), GRAY))

        #Define horizontal lines
        for i in range(NROWS):
            self.grid.append(Line(Vector2(0, i*TILEHEIGHT),Vector2(SCREENWIDTH, i*TILEHEIGHT), GRAY))

    def update(self):
        '''Main game loop'''
        x, y = pygame.mouse.get_pos()
        mouseposition = Vector2(x, y)

        self.hoverVertex = None
        for vertex in self.vertices.values():
            if vertex.inbounds(mouseposition):
                self.hoverVertex = vertex

        if self.editMode:
            if self.hoverVertex is not None:
                if self.followMouse:
                    self.hoverVertex.position = mouseposition

        if self.probeMode:
            if self.probe is not None:
                if self.followMouse:
                    self.probe.position = mouseposition
                
        if self.vertexShadow is not None:
            self.vertexShadow.update(mouseposition)

        if self.connectionLine is not None:
            self.connectionLine.vector1 = mouseposition
        
        self.events.update(mouseposition)
        self.render()

    def getVertex(self, position):
        '''Return the key to the vertex that matches the position.  Return None if no matches.'''
        for key in self.vertices.keys():
            if self.vertices[key].position == position:
                return key
        return None
    
    def getAllSegments(self):
        '''Just returns a list of all of the segments.  [(1,2), (2,3), (4,5), ...].
        as SegmentDirected objects.'''
        segments = []
        for key in self.vertices.keys():
            for i in range(len(self.vertices[key].neighbors)):
                segments.append(Segment(self.vertices[key], self.vertices[key].neighbors[i]))
        return segments

    def createBinaryTree(self):
        '''Performs the steps necessary to split the segments into a space partitioned binary tree. PRESS B'''
        self.segments = self.getAllSegments()
        self.bsp = BSP(self.segments)
        self.bsp.createTree() #just for testing.  Normally doesn't return anything
        self.segments = self.bsp.segments
        
    def createVertex(self, position):
        '''Create a new vertex and add it to the dictionary'''
        vertex = Vertex(position, key=self.vertex_key_ctr)
        self.vertices[self.vertex_key_ctr] = vertex
        self.vertex_key_ctr += 1
        self.vertexShadow = None
        
    def createVertexShadow(self, position):
        self.vertexShadow = VertexShadow(position)

    def createConnectionLine(self):
        '''The line that is shown when connecting two nodes together.  vertex0 is where the line is anchored'''
        self.vertex0 = self.hoverVertex
        position = self.hoverVertex.position
        self.connectionLine = Line(position, position, RED)

    def connectVerticesDirected(self):
        '''Only vertex 1 knows about vertex 2'''
        self.vertex0.addNeighbor(self.hoverVertex)
        
    #def connectVerticesUndirected(self):
        '''Connect two vertices together such that they are neighbors of each other'''
    #    print("Undirected")
        #print(str(self.vertex0.key) + " <==> " + str(self.hoverVertex.key))
    #    self.vertex0.addNeighbor(self.hoverVertex)
    #    self.hoverVertex.addNeighbor(self.vertex0)
        
    def removeNeighbors(self):
        '''Remove all the neighbors from the vertices'''
        for vertex in self.vertices.values():
            vertex.neighbors = []

    def render(self):
        if self.editMode:
            self.screen.blit(self.background_edit, (0,0))
        elif self.connectionMode:
            self.screen.blit(self.background_connection, (0,0))
        elif self.checkMode:
            self.screen.blit(self.background_check, (0,0))
        elif self.probeMode:
            self.screen.blit(self.background_probe, (0,0))
        else:
            self.screen.blit(self.background, (0,0))
            
        if self.showGrid:
            for line in self.grid:
                line.render(self.screen)

        if self.connectionLine is not None:
            self.connectionLine.render(self.screen)
    
        for vertex in self.vertices.values():
            vertex.renderConnections(self.screen)
            
        if self.showVertices:
            for vertex in self.vertices.values():
                vertex.render(self.screen)

        if self.vertexShadow is not None:
            self.vertexShadow.render(self.screen)

        #This is just to show where the line splits will be made when doing bsp
        if len(self.testvertexlist) > 0:
            #self.testvertexlist.render(self.screen)
            for b in self.testvertexlist:
                b.render(self.screen)
                #x, y = int(b.x), int(b.y)
                #pygame.draw.circle(self.screen, (0, 155, 0), (x, y), 5)

        if len(self.segments) > 0:
            for seg in self.segments:
                seg.render(self.screen)
                
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.defineGrid()
    while True:
        game.update()
