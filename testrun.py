import pygame
from constants import *
from Primitives.vectors import Vector2
from Primitives.segment import Segment
from events import EventManager
from bsp import BinarySpacePartitioner as BSP
import testsectors
from player import Player
from wallrender import WallRender3D

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
        self.mousePosition = None
        self.bsp = None
        self.testvertexlist = []
        self.segments = [] #make global for testing so we can see them dynamically
        self.events = EventManager(self)
        self.player = None
        self.WR3D = None
        self.mode3D = False
        
    def update(self):
        '''Main game loop'''
        #dt = self.clock.tick(30) / 1000.0
        x, y = pygame.mouse.get_pos()
        self.mouseposition = Vector2(x, y)
        self.events.update(self.mouseposition)
        self.render()

    def getTestSector(self):
        '''From the testsectors file.  Press button 5'''
        L = testsectors.sector2()
        print(L)
        self.segments = []
        for pair in L:     
            v1 = Vector2(pair[0])
            v2 = Vector2(pair[1])
            self.segments.append(Segment(v1, v2, name=pair[2]))

        self.bsp = BSP(self.segments)
        self.bsp.createTree()
        
    def stepThroughTree(self):
        '''This just helps me step through the tree one iteration at a time to see what it is doing for debugging.'''
        self.bsp.traverseTree()

    def createPlayer(self):
        '''Create a player in the middle of the screen'''
        #self.getSegmentDrawingOrder(self.mouseposition)
        if self.player is None and self.bsp is not None:
            self.player = Player(SCREENWIDTH/2, SCREENHEIGHT/2)
            self.WR3D = WallRender3D(self.bsp.tree, self.player)

    def render(self):
        self.screen.blit(self.background, (0,0))

        if not self.mode3D:
            if len(self.segments) > 0:
                for seg in self.segments:
                    seg.render(self.screen)
        
        if self.player is not None:
            if self.mode3D:
                self.WR3D.render(self.screen)
            else:
                self.player.render(self.screen)
            
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    while True:
        game.update()

