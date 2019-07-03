import pygame
from constants import *
from Primitives.vectors import Vector2
from Primitives.lines import Line

"""+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
A segment has two points.  It just forms a straight line between these two points.  We do not have to actually draw this.  I draw the segments in a better way.  This just exists in order to determine the point of intersection between 2 Segments.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
class Segment(object):
    def __init__(self, position1, position2):
        '''The inputs can be either Vector2 or a list or a tuple of 2 elements.  Need to determine which and force them to be Vector2s.'''
        self.p1 = self.determineType(position1)
        self.p2 = self.determineType(position2)

    def __str__(self):
        '''Return a string representation of a Segment'''
        return str(self.p1) + "------" + str(self.p2)

    def determineType(self, value):
        '''Determine the type of the value.  This allows us to create a Segment using vectors, tuples, or lists.  We want to return the Vector2 representation.'''
        if type(value) is tuple or type(value) is list:
            x, y = value
            return Vector2(x, y)
        elif type(value) is Vector2:
            return value
        return None

    def vectorBetweenPoints(self):
        '''Gets the vector that is formed between the two p1 and p2 vectors.  Points from p1 to p2'''
        return self.p2 - self.p1
    
    def intersectSegment(self, other):
        '''Segment-Segment intersection.  Segments physically intersect each other'''
        p = self.vectorBetweenPoints()
        q = other.vectorBetweenPoints()
        if float(p.cross(q)) != 0:
            q_p = other.p1 - self.p1
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            if 0 < s < 1 and 0 < t < 1:
                return True
        return False

    def intersectRay(self, ray):
        '''Segment-Ray intersection'''
        pass

    def intersect(self, other):
        '''Determine where 2 Segment objects intersect.  If they don't intersect, just return None.'''
        p = self.vectorBetweenPoints()
        q = other.vectorBetweenPoints()
        if float(p.cross(q)) != 0:
            q_p = other.p1 - self.p1
            s = q_p.cross(q) / float(p.cross(q))
            t = q_p.cross(p) / float(p.cross(q))
            if 0 < s < 1:
                return s, t
        return None, None

    def parallel(self, other):
        '''Check if this segment is parallel with the other segment'''
        p = self.vectorBetweenPoints()
        q = other.vectorBetweenPoints()
        if float(p.cross(q)) == 0:
            return True
        return False

    def midpoint(self):
        '''Return the midpoint of this sector.  The midpoint is a Vector2'''
        vec = self.p1 + self.p2
        return vec / 2


class SegmentDirected(Segment):
    def __init__(self, vertex1, vertex2):
        Segment.__init__(self, vertex1.position, vertex2.position)
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __str__(self):
        return str(self.vertex1.key) + "---->"+str(self.vertex2.key)

    def __eq__(self, other):
        if self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2:
            return True
        return False

    def __hash__(self):
        return id(self)
    
    def intersectAsRay(self, other, reverse=False):
        '''Turn this segment into a line and see if it instersects other SegmentDirected objects'''
        line = Line(self.p1, self.p2)
        ray = line.getRay(reverse=reverse)
        #ray2 = line.getRay(reverse=True)
        #s1 = ray1.intersectSegmentAt(segment)
        #s2 = ray2.intersectSegmentAt(segment)
        s = ray.intersectSegmentAt(other)
        if s is None:
            return None
        else:
            if reverse:
                pos = self.p2
                #splitPosition = self.p2 + ray.direction*s
            else:
                pos = self.p1
            splitPosition = pos + ray.direction*s
            return pos, splitPosition

            
        #if s1 == None and s2 == None:
        #    return None
        #else:
            #self.showSplit = True
        #    if s1 is not None:
        #        splitPosition = self.p2 + direction1*s1
                #tempSegment = Segment(self.vector1, splitPosition)
                #print("s1 = " + str(s1) + " vector1 = " + str(self.vector1))
                #print(str(self.vector0) + " ------> " + str(splitPosition))
        #        return self.p1, splitPosition
        #    elif s2 is not None:
        #        splitPosition = self.p1 + direction2*s2
                #tempSegment = Segment(self.vector0, splitPosition)
                #print("s2 = " + str(s2) + " vector0 = " + str(self.vector0))
                #print(str(self.vector1) + " ------> " + str(splitPosition))
        #        return self.p2, splitPosition
            #return (self.p2, splitPosition1), (self.p1, splitPosition2)
        
        #result = line.intersectSegment(other)
        #if result is not None:
        #    pass
        #return result

    
