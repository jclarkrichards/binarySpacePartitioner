import pygame
import utils
from constants import *
from Primitives.vectors import Vector2
from Primitives.lines import Line
from Primitives.vertex import Vertex
from Primitives.ray import Ray

"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
A segment has two points.  It just forms a straight line between these two points.  We do not have to actually draw this.  I draw the segments in a better way.  This just exists in order to determine the point of intersection between 2 Segments.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
class Segment(object):
    def __init__(self, vertex1, vertex2):
        '''The input objects should be of type Vertex since a segment contains 2 Vertex objects in order to define it.  A segment is a directed segment and points from vertex1 to vertex2.'''
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.vector = self.vertex2.position - self.vertex1.position
        
    def __str__(self):
        '''Return a string representation of a Segment'''
        return str(self.vertex1.key) + " ---> " + str(self.vertex2.key)

    def __eq__(self, other):
        '''Two segments are equal if they have the same vertices'''
        if self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2:
            return True
        return False

    def __hash__(self):
        return id(self)

    def getRay(self):
        '''Return a Ray representation of this Segment'''
        return Ray(self.vertex1.position, self.vector)
    
    def intersectSegment(self, other):
        '''Segment-Segment intersection.  Segments physically intersect each other'''
        #print("Does this even happen?")
        s, t = utils.intersect(self.vertex1.position, other.vertex1.position, 
                               self.vector, other.vector)
       
        if 0 < s < 1 and 0 < t < 1:
            return True
        return False

    def parallel(self, other):
        '''Check if this segment is parallel with the other segment'''
        if float(self.vector.cross(other.vector)) == 0:
            return True
        return False

    def midpoint(self):
        '''Return the midpoint of this sector.  The midpoint is a Vector2'''
        return (self.vertex1.position + self.vertex2.position) / 2.0

    def intersectAsRay(self, other):
        '''Turn this segment into a ray and see if it instersects other Segment objects'''
        ray = self.getRay()
        s = ray.intersectSegment(other)
        if s is not None:
            splitPosition = ray.position + ray.direction*s
            vertex = Vertex(splitPosition)
            #return splitPosition
            if s > 0:
                return Segment(self.vertex2, vertex)
            elif s < 0:
                return Segment(self.vertex1, vertex)
        else:
            return None
        
            #if reverse:
            #    pos = self.vertex2.position
            #else:
            #    pos = self.vertex1.position
            #splitPosition = pos + ray.direction*s
            #return pos, splitPosition



    
