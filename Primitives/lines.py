import pygame
from constants import *
from Primitives.vectors import Vector2
from Primitives.ray import Ray

"""A Line is like a segment in that it has a start and end that defines the line, but it does not depend on the vertex dictionary.  It is just an all-purpose Segment that can be used for non-vertex stuff.  Instead of vertices, we use vectors."""
class Line(object):
    def __init__(self, vector0, vector1, color=WHITE):
        self.vector0 = vector0
        self.vector1 = vector1
        self.color = color
        self.thickness = 1
        
    def getVector(self):
        pass

    def getRay(self, reverse=False):
        '''Return a Ray representation of this line.  This can result in 1 of 2 rays.  Normally the ray will point from vector0 --> vector1.  Setting reverse to True will point vector1 --> vector0.'''
        if reverse:
            vec = self.vector0 - self.vector1
            direction = vec.normalize()
            ray = Ray(self.vector1, direction)
        else:
            vec = self.vector1 - self.vector0
            direction = vec.normalize()
            ray = Ray(self.vector0, direction)
        return ray
        

    def intersectSegment(self, segment):
        '''Similar to how a Ray intersects a segment, but a line intersects a segment in both directions.  In fact, we just create a Ray for both directions and use that.'''
        ray1 = self.getRay()
        ray2 = self.getRay(reverse=True)
        #vec1 = self.vector0 - self.vector1
        #direction1 = vec1.normalize()
        #vec2 = self.vector1 - self.vector0
        #direction2 = vec2.normalize()
        #ray1 = Ray(self.vector1, direction1)
        #ray2 = Ray(self.vector0, direction2)
        s1 = ray1.intersectSegmentAt(segment)
        s2 = ray2.intersectSegmentAt(segment)
        if s1 == None and s2 == None:
            return None
        else:
            #self.showSplit = True
            if s1 is not None:
                splitPosition = self.vector1 + direction1*s1
                print("s1 = " + str(s1) + " vector1 = " + str(self.vector1))
                print(str(self.vector0) + " ------> " + str(splitPosition))
                return self.vector0, splitPosition
            elif s2 is not None:
                splitPosition = self.vector0 + direction2*s2
                print("s2 = " + str(s2) + " vector0 = " + str(self.vector0))
                print(str(self.vector1) + " ------> " + str(splitPosition))
                return self.vector1, splitPosition
            #return True
    
    def render(self, screen):
        pygame.draw.line(screen, self.color, self.vector0.toTuple(),
                         self.vector1.toTuple(), self.thickness)
