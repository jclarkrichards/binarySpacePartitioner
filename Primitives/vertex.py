import pygame
from constants import *
from Primitives.vectors import Vector2

"""A Vertex is just a point in space with an x and y position.  Visually (when drawing) it is a red circle.  All of the vertices are stored in a dictionary, so the key variable is the key in the dictionary this vertex is found.  This value does not change.  The position is just a Vector2.  The neighbors list is a list of Vertex objects that this Vertex points to."""
class Vertex(object):
    def __init__(self, position, key=0):
        self.key = key
        self.position = position
        self.neighbors = []
        self.color = RED
        self.radius = 10 #for display and mouse detection

    def __str__(self):
        '''Print out a representation of this vertex'''
        return "Vertex " + str(self.key) + " :: " + str(self.position)
        
    def __eq__(self, other):
        '''2 vertices are the same if they have the same position'''
        return self.position == other.position

    def __hash__(self):
        '''Required in Python 3'''
        return id(self)
    
    def addNeighbor(self, vertex):
        '''Add a neighbor to the list if not already in list'''
        keys = [k.key for k in self.neighbors]
        #print("Vertex " + str(self.key) + " ===> " + str(keys))
        if vertex.key not in keys and vertex.key != self.key:
            #print("add vertex " + str(vertex.key) + " as neighbor to vertex " + str(self.key))
            self.neighbors.append(vertex)

    def removeNeighbor(self, vertex):
        '''Remove a vertex from the neighbor list'''
        if vertex in self.neighbors:
            self.neighbors.remove(vertex)
            
    def getPosition(self):
        '''Return a copy of this position for some reason'''
        return self.position.copy()
    
    def inbounds(self, mousepos):
        '''Allows for mouse detection when a mouse is hovering over.  If a mouse is hovering over this vertex, then turn it green'''
        x, y = mousepos.toTuple()
        self.color = RED
        if self.position.x-self.radius < x < self.position.x+self.radius:
            if self.position.y-self.radius < y < self.position.y+self.radius:
                self.color = GREEN
                return True
        return False

    def renderConnections(self, screen):
        '''Draw the lines that connect this vertex to the neighbors'''
        for vertex in self.neighbors:
            pygame.draw.line(screen, SEGMENTCOLOR, self.position.toTuple(), vertex.position.toTuple(), 1) 

    def intersectSegment(self, sector):
        '''Segment-Vertex intersection.  Segment must physically cross vertex.  '''
        pass

    def intersectRay(self, ray):
        '''Ray-Vertex intersection.  Ray does not physically cross vertex.'''
        pass
    
    def render(self, screen):
        '''Draw this vertex as a RED circle'''
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)


"""A VertexShadow object is just a simple circle that is created when we press the mouse down to create a vertex.  When we release the mouse, this is destroyed and a real Vertex takes its place"""
class VertexShadow(object):
    def __init__(self, position):
        self.position = position
        self.color = RED
        self.radius = 10 #for display and mouse detection

    def update(self, position):
        '''Always follows the mouse'''
        self.position = position
        
    def render(self, screen):
        '''Draw this vertex as a RED circle'''
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.circle(screen, (200,50,0,100), (x, y), self.radius)


class Probe(object):
    def __init__(self, position):
        self.position = position

    def render(self, screen):
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.circle(screen, (200,100,0), (x, y), 10)
    
        
          
