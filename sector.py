import pygame
from constants import *
from Primitives.vectors import Vector2
from Primitives.lines import Segment, Ray, SegmentDirected
from Primitives.vertex import Vertex
from copy import deepcopy
"""A sector is an area that is defined by a set of vertices.  We can check to see if this sector is convex or concave"""

class Sector(object):
    def __init__(self, vertices, cycle, sequence=None):
        self.midpoint = None
        self.vertices = vertices
        if cycle is not None:
            self.sequence = cycle.sequence
        elif sequence is not None:
            self.sequence = sequence
        self.positions = [] #position Vector2 of each sequence in the sector
        self.color = BLUE
        if len(vertices) > 0:
            self.setPositionList(vertices)

    def __str__(self):
        return str(self.sequence) + " : " + str(len(self.sequence))
    
    def setPositionList(self, vertices):
        for i in range(len(self.sequence)):
            self.positions.append(vertices[self.sequence[i]].position)
        
    def convexOrConcave(self):
        '''Check if this sector is convex or concave.  Just need the position list.  Return True if convex'''
        indexlist = list(range(len(self.positions))) + [0, 1]
        positives = []
        negatives = []
        for i in range(len(self.positions)):
            vector1 = self.positions[indexlist[i+1]] - self.positions[indexlist[i]]
            vector2 = self.positions[indexlist[i+2]] - self.positions[indexlist[i+1]]
            cross = vector1.cross(vector2)
            if cross >= 0:
                positives.append(cross)
            else:
                negatives.append(cross)

        if len(positives) == 0 or len(negatives) == 0:
            return True
        return False

    def splitSector(self):
        '''Split this sector by joining two vertices together.  Pick a vertex and then join its neighbors together iff the line that joins those neighbors is inside the sector.'''
        print("---------------------Splitting Sector------------------------")
        print(self.sequence)
        midpoint = None
        for key in self.sequence:
            n1, n2 = self.getNeighbors(key)
            print("Vertex " + str(key) + " has Neighbors: " + str(n1) + ", " + str(n2))
            #print("Check that there are no line crossings first between "+str(n1)+ " and " + str(n2))
            intersects = self.checkIntersections(n1, n2)
            if not intersects:
                self.midpoint = self.getMidpoint(n1, n2)
                print("Check if midpoint is inside sector: " + str(self.midpoint))
                #print("")
                inside = self.pointInsideSector(self.midpoint)
                if inside:
                    print("+++++++++++++++++++midpoint is inside sector, so connect them")
                    print(self.midpoint)
                    self.connectVertices(n1, n2)
                    break
            print("")
            
    def getNeighbors(self, key):
        '''Given a key, return the left and right values from the self.sequence list'''
        index = self.sequence.index(key)
        n1 = self.sequence[(index+1) % len(self.sequence)]
        n2 = self.sequence[index-1]
        return n1, n2

    def getMidpoint(self, key1, key2):
        '''Get the midpoint vector between key1 and key2'''
        position1 = self.vertices[key1].position
        position2 = self.vertices[key2].position
        return (position1 + position2) / 2.0

    def checkIntersections(self, key1, key2):
        '''Check if connecting these two vertices by a line would intersect any existing lines within the sector'''
        print("--------------CHECKING INTERSECTION CROSSINGS-------------------")
        print(str(key1) + "------------"+str(key2))
        print("----------------------------------------------------------------")
        position1 = self.vertices[key1].position
        position2 = self.vertices[key2].position
        segment = Segment(position1, position2)
        tempList = self.sequence + [0]
        print("Loop through list: " + str(tempList))
        for i in range(len(self.sequence)):
            k1 = tempList[i]
            k2 = tempList[i+1]
            p1 = self.vertices[k1].position
            p2 = self.vertices[k2].position
            print("check " + str(k1) + " and " + str(k2))
            segment_test = Segment(p1, p2)
            intersecting = segment.intersectSegment(segment_test)
            if intersecting:
                print(str(key1) + " and " + str(key2) + " intersects " + str(k1) + " and " + str(k2))
                return True
        return False
    
    def pointInsideSector(self, point):
        '''point is a Vector2.  Check if a point is inside the sector or outside the sector.  Create a ray that points to the right.  Loop through each segment that makes up this sector and count how many sectors this ray crosses.  If that number is odd, the point is inside the sector.  If even, the point is outside.'''
        xvector = Vector2(1,0)
        ray = Ray(point, xvector)
        num_crossings = 0
        tempList = self.sequence + self.sequence[0:1]
        for i in range(len(self.sequence)):
            k1 = tempList[i]
            k2 = tempList[i+1]
            p1 = self.vertices[k1].position
            p2 = self.vertices[k2].position
            segment = Segment(p1, p2)
            if ray.intersectSegment(segment):
                num_crossings += 1
        print("For point " + str(point) + " # of crossings = " + str(num_crossings))
        if self.evenValue(num_crossings):
            return False
        return True
    
    def evenValue(self, value):
        '''Return True if the value is even, False if odd'''
        return not value % 2
    
    def connectVertices(self, key1, key2):
        '''Connect these two vertices together'''
        self.vertices[key1].addNeighbor(self.vertices[key2])
        self.vertices[key2].addNeighbor(self.vertices[key1])
    
    def render(self, screen):
        positionList = []
        for p in self.positions:
            positionList.append(p.toTuple())
        pygame.draw.polygon(screen, self.color, positionList)

    def renderMidpoint(self, screen):
        if self.midpoint is not None:
            x, y = self.midpoint.toTuple()
            pygame.draw.circle(screen, (200,0,200), (int(x), int(y)), 5)
    

            
"""Use this when doing the BSP step. Does things slightly differently than the Sector above"""
class SectorBSP(object):
    def __init__(self, segments):
        print("----SectorBSP-----")
        self.segments = segments
        for seg in self.segments:
            print(seg)
        self.loops = []
        self.sortSegments()

    def sortSegments(self):
        '''It is not guaranteed that the segments will be in any particular order.  By restrictions, the segments should form 1 or more closed loops.'''
        segments = deepcopy(self.segments)
        while len(segments) > 0:
            loop = []
            seg = segments.pop(0)
            loop.append(seg)
            loopfound = False

            while not loopfound: # or num == 10:
                for segment in segments:
                    if segment.vertex1.key == seg.vertex2.key:
                        loop.append(segment)
                        if segment.vertex2.key == loop[0].vertex1.key:
                            loopfound = True
                        seg = segment
                        segments.remove(segment)
                        break
                   
            self.loops.append(loop)
            
        #print("There are " + str(len(self.loops)) + " loops")
        #for loop in self.loops:
        #    print("----LOOP-----")
        #    for seg in loop:
        #        print(seg)
        #isconvex = self.convexOrConcave()
        #print("Is convex = " + str(isconvex))
        
    def convexOrConcave(self):
        '''Check if the segments define a convex or concave area'''
        isconvex = True
        for loop in self.loops:
            temploop = loop + [loop[0]]
            for i in range(len(loop)):
                vector1 = temploop[i].vertex2.position - temploop[i].vertex1.position
                vector2 = temploop[i+1].vertex2.position - temploop[i+1].vertex1.position
                if vector1.cross(vector2) < 0:
                    isconvex = False
                    break
                
        return isconvex

    def electBestSegment(self):
        '''The best segment is the segment that can divide this sector into 2 sectors as equally as possible'''
        test = []
        for segment in self.segments:
            print("=====================================================")
            print("Checking segment " + str(segment) + " against other segments")
            print("=====================================================")
            for other in self.segments:
                if other is not segment:
                    #print("-------------------------------")
                    #print(other)
                    #result = segment.intersectAsLine(other)
                    result1 = segment.intersectAsRay(other)
                    result2 = segment.intersectAsRay(other, reverse=True)
                    if result1 is not None:
                        test.append(result1[1])
                        
                    elif result2 is not None:
                        test.append(result2[1])
                    
                    #if result is not None:
                    #    print("Intersects " + str(other))
                        
                        #test.append(intersects[1])
        return test


    
