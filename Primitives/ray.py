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

    def intersectSegment(self, segment, includeEndpoints=False):
        '''Returns the s value indicating where the intersection is occuring on the segment.  If no intersection, then None is returned. If s is negative, then the intersection is happening behind it.'''
        s, t = utils.intersect(self.position, segment.p1, self.direction, segment.vector)
        if includeEndpoints:
            #print("s, t = " + str(s) + ", " + str(t))
            if 0 <= t <= 1:
                if s != 0 and s != 1: #still need to ignore endpoints where this segment is connected to 
                    return s
        else:
            if 0 < t < 1:
                return s
        return None

    def intersectSegmentRaw(self, segment):
        '''Same as above, but instead we are only looking ahead of ray not behind and we want full range of t: 0<=t<=1'''
        s, t = utils.intersect(self.position, segment.p1, self.direction, segment.vector)
        if s > 0:
            return t
        return None

    

    
