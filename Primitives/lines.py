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

    
"""A Line is like a segment in that it has a start and end that defines the line, but it does not depend on the vertex dictionary.  It is just an all-purpose Segment that can be used for non-vertex stuff.  Instead of vertices, we use vectors."""
class Line(object):
    def __init__(self, vector0, vector1, color=WHITE):
        self.vector0 = vector0
        self.vector1 = vector1
        self.color = color
        self.thickness = 1
        #self.splitPosition = None
        #self.showSplit = False
        
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
        #print("drawing lines")
        pygame.draw.line(screen, self.color, self.vector0.toTuple(),
                         self.vector1.toTuple(), self.thickness)
        #if self.showSplit:
        #    x = int(self.splitPosition.x)
        #    y = int(self.splitPosition.y)
        #    pygame.draw.circle(screen, (0,150,0), (x, y), 5) 

    
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

    
