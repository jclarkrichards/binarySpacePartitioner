import pygame
from constants import *
from Primitives.vectors import Vector2
import utils

"""A Ray is something that has a position and points in a certain direction to infinity.  Both position and direction are Vector2 objects.  The direction is unit vector."""
class Ray(object):
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction.normalize()
        
    def parallel(self, other):
        '''Check if this ray is parallel with another ray'''
        if float(self.direction.cross(other.direction)) == 0:
            return True
        return False
    
    def parallelSegment(self, segment):
        '''Check if this ray is parallel with a segment'''
        other = segment.getRay()
        return self.parallel(other)

    def intersectSegment(self, segment):
        '''Returns the s value indicating where the intersection is occuring on the segment.  If no intersection, then None is returned. If s is negative, then the intersection is happening behind it.'''
        s, t = utils.intersect(self.position, segment.p1, self.direction, segment.vector)
        if 0 < t < 1:
            return s
        return None

    

    
