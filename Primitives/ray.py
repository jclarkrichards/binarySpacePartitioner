import pygame
from constants import *
from Primitives.vectors import Vector2

"""A Ray is something that has a position and points in a certain direction to infinity.  Both position and direction are Vector2 objects"""
class Ray(object):
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def parallelSegment(self, segment):
        '''Check if this ray is parallel with a segment'''
        p = self.direction
        q = segment.vectorBetweenPoints()
        if float(p.cross(q)) == 0:
            return True
        return False

    def intersectRay(self, segment):
        '''Ray-Ray intersection'''
        pass
    
    def intersectSegment(self, segment, ignoreVertices=False):
        '''Ray-Segment intersection.  Test to see if this ray intersects with a segment.  Just return True of False.  If intersecting the segment at one of its vertices, then we say we intersect it only if the other vertex is above this ray.'''
        p = self.direction
        q = segment.vectorBetweenPoints()
        if float(p.cross(q)) != 0:
            q_p = segment.p1 - self.position
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            s = round(s, 5)
            t = round(t, 5)
            if s == 0.0:
                s = abs(s)
            if t == 0.0:
                t = abs(t)
            #print("s="+str(s)+"      t="+str(t))
            if s > 0:
                if 0 < t < 1:
                    return True
                elif t == 0 or t == 1: # intersecting at the vertex
                    if ignoreVertices:
                        return False
                    else:
                        if segment.p1.y == self.position.y:
                            if segment.p2.y < self.position.y:
                                return True
                        elif segment.p2.y == self.position.y:
                            if segment.p1.y < self.position.y:
                                return True
        return False

    def intersectSegmentAt(self, segment):
        '''Same as above, except instead of returning True or False, it returns the s value indicating where the intersection is occuring on the segment.  If no intersection, then None is returned.'''
        p = self.direction
        q = segment.vectorBetweenPoints()
        if float(p.cross(q)) != 0:
            q_p = segment.p1 - self.position
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            s = round(s, 5)
            t = round(t, 5)
            if s == 0.0:
                s = abs(s)
            if t == 0.0:
                t = abs(t)
            if s > 0:
                if 0 < t < 1:
                    return s
        return None

    

    
