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
    def __init__(self, vector1, vector2, virtual=False, name=""):
    #def __init__(self, vertex1, vertex2, virtual=False):
        '''The input objects should be of type Vertex since a segment contains 2 Vertex objects in order to define it.  A segment is a directed segment and points from vertex1 to vertex2.'''
        self.name = name
        self.p1 = vector1
        self.p2 = vector2
        #self.vertex1 = vertex1
        #self.vertex2 = vertex2
        #self.vector = self.vertex2.position - self.vertex1.position
        self.vector = self.p2 - self.p1
        self.direction = self.vector.normalize()
        self.direction = utils.clampVector(self.direction, 2)
        self.virtual = virtual
        
        
    def __str__(self):
        '''Return a string representation of a Segment'''
        return self.name + " : " + str(self.p1) + " ---> " + str(self.p2)

    def __eq__(self, other):
        '''Two segments are equal if they have the same vertices'''
        if self.p1 == other.p1 and self.p2 == other.p2:
            return True
        return False

    def __hash__(self):
        return id(self)

    def getRay(self):
        '''Return a Ray representation of this Segment'''
        return Ray(self.p1, self.vector)

    def intersectVector(self, pos, vec):
        '''Does this segment intersect a vector?'''
        s, t = utils.intersect(self.p1, pos, self.vector, vec)
        #print(self.name + " intersects " + other.name + " using (s, t) -> ("+str(s)+", "+str(t)+")")
        print("s="+str(s)+", t="+str(t))
        if 0 < s < 1 and t >= 0:
            return True
        return False
        
    def intersectSegment(self, other, includeEndpoints=False):
        '''Segment-Segment intersection.  Segments physically intersect each other'''
        s, t = utils.intersect(self.p1, other.p1, self.vector, other.vector)
        #print(self.name + " intersects " + other.name + " using (s, t) -> ("+str(s)+", "+str(t)+")")
        if includeEndpoints:
            if 0 < s < 1 and 0 <= t <= 1:
                return True
        else:
            if 0 < s < 1 and 0 < t < 1:
                return True
        return False

    def getOtherIntersectionValue(self, other, includeEndpoints=False):
        '''Get the value of intersection for the other segment where this segment has its endpoint on the other segment'''
        s, t = utils.intersect(self.p1, other.p1, self.vector, other.vector)
        #print(self.name + " intersects " + other.name + " using (s, t) -> ("+str(s)+", "+str(t)+")")
        if includeEndpoints:
            if (s == 0 or s == 1) and 0 <= t <= 1:
                return t
        else:
            if (s == 0 or s == 1) and 0 < t < 1:
                return t
        return None
        
    def intersectSegmentEndpoints(self, other):
        '''In a special case we want to know when this segment is intersecting the other segment only at this segments endpoints'''
        #print("Checking endpoint intersections")
        #print(self.name + " ..... " + other.name)
        s, t = utils.intersect(self.p1, other.p1, self.vector, other.vector)
        if (s == 0 or s == 1) and 0 < t < 1:
            return t
        return None
            
    def parallel(self, other):
        '''Check if this segment is parallel with the other segment'''
        if float(self.vector.cross(other.vector)) == 0:
            return True
        return False

    def midpoint(self):
        '''Return the midpoint of this sector.  The midpoint is a Vector2'''
        return (self.p1 + self.p2) / 2.0

    def otherSegmentConnected(self, other):
        '''Need to know if the other segment is connected to this segment.  If we test intersection including endpoints, then the other segment is connected if the intersection is at this segements endpoints where s = 0 or s = 1'''
        s, t = utils.intersect(self.p1, other.p1, self.vector, other.vector)
        #print("connection check: " + str(s) + ", " + str(t))
        if (s == 0 or s == 1) and (t == 0 or t == 1):
            return True
        return False
        
    def intersectAsRay(self, other, includeEndpoints=False):
        '''Turn this segment into a ray and see if it instersects other Segment objects'''
        connectedSegment = self.otherSegmentConnected(other)
        if not connectedSegment:
            ray = self.getRay()
            s = ray.intersectSegment(other, includeEndpoints)
            if s is not None:
                splitPosition = ray.position + ray.direction*s
                splitPosition = utils.clampVector(splitPosition, 0)
                if s > 0:
                    return Segment(self.p2, splitPosition, True, self.name+"_#")
                elif s < 0:
                    return Segment(splitPosition, self.p1, True, self.name+"_#")
            else:
                return None
        
    def split(self, other):
        '''Split this segment into 2 segments.  We really just create 1 new Segment and then modify this segment.'''
        s, t = utils.intersect(self.p1, other.p1, self.vector, other.vector)
        if t == 0: #other.p1 intersects this segment
            segment2 = Segment(other.p1, self.p2, self.virtual, self.name+"_2")
            self.p2 = other.p1
            #segment1 = Segment(self.p1, other.p1, self.virtual)
            
        elif t == 1: #other.p2 intersects this segment
            segment2 = Segment(other.p2, self.p2, self.virtual, self.name+"_2")
            self.p2 = other.p2
            #segment1 = Segment(self.p1, other.p2, self.virtual)

            

        return segment2

    def reverse(self):
        '''Return a new segment that is just the reverse of this segment'''
        return Segment(self.p2, self.p1, self.virtual, self.name+"_r")


    def side(self, position):
        '''Which side of the segment is the position?  Return "left" or "right"'''
        p = position - self.p1
        value = self.vector.cross(p)
        if value >= 0:
            return "right"
        return "left"
    
    def render(self, screen):
        x, y = self.p2.toTuple()
        x, y = int(x), int(y)
        if self.virtual:
            color = (255,255,255)
        else:
            color = (255,255,0)
        
        pygame.draw.line(screen, color, self.p1.toTuple(), self.p2.toTuple(), 3)
        pygame.draw.circle(screen, (0, 150, 0), (x, y), 5)

    
