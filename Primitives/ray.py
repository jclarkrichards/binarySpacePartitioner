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

    def intersectRay(self, other):
        '''Ray-Ray intersection'''
        pass
    
    def intersectSegmentOLD(self, segment, ignoreVertices=False):
        '''Ray-Segment intersection.  Test to see if this ray intersects with a segment.  Just return True of False.  If intersecting the segment at one of its vertices, then we say we intersect it only if the other vertex is above this ray.'''
        p = self.direction
        q = segment.vector
        if float(p.cross(q)) != 0:
            q_p = segment.vertex1.position - self.position
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            s = utils.clamp(s, 5)
            t = utils.clamp(t, 5)
            if s > 0:
                if 0 < t < 1:
                    return True
                elif t == 0 or t == 1: # intersecting at the vertex
                    if ignoreVertices:
                        return False
                    else:
                        if segment.vertex1.position.y == self.position.y:
                            if segment.vertex2.position.y < self.position.y:
                                return True
                        elif segment.vertex2.position.y == self.position.y:
                            if segment.vertex1.position.y < self.position.y:
                                return True
        return False

    def intersectSegment(self, segment):
        '''Returns the s value indicating where the intersection is occuring on the segment.  If no intersection, then None is returned.'''
        p = self.direction
        q = segment.vector
        if float(p.cross(q)) != 0:
            q_p = segment.vertex1.position - self.position
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            s = utils.clamp(s, 5)
            t = utils.clamp(t, 5)
            if s > 0:
                if 0 < t < 1:
                    return s
        return None

    

    
