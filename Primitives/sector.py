import pygame
from constants import *
from Primitives.vectors import Vector2
from Primitives.segment import Segment
from Primitives.ray import Ray
from Primitives.vertex import Vertex
from copy import deepcopy
import utils
"""A sector is an area that is defined by a list of Segment objects.  We can check to see if this sector is convex or concave"""

"""Use this when doing the BSP step. Does things slightly differently than the Sector above"""
class Sector(object):
    def __init__(self, segments):
        print("----SectorBSP-----")
        self.segments = segments
        #for seg in self.segments:
        #    print(seg)
        print("______________________________")
        self.segments = self.sortSegments()
        #for seg in self.segments:
        #    print(seg)

    def sortSegments(self):
        '''It is not guaranteed that the segments will be in any particular order.  By restrictions, the segments should form 1 closed loop.  
        This does not happen unless we know ahead of time that we have a single closed loop.'''
        #print("Sorting segments")
        segments = deepcopy(self.segments)
        temp = []
        seg = segments.pop(0)
        temp.append(seg)
        #print("Number of segments to sort = " + str(len(segments)))
        while len(segments) > 0:
            #print(len(segments))
            for segment in segments:
                #print(str(segment.vertex1.position), str(seg.vertex2.position))
                if segment.p1 == seg.p2:
                    temp.append(segment)
                    seg = segment
                    segments.remove(segment)
                    break
        return temp
        
    def convexOrConcave(self):
        '''Check if the segments define a convex or concave area'''
        #print("=======CONCAVITY CHECKING START===========")
        segments = self.segments + [self.segments[0]]
        isconvex = True
        for i in range(len(self.segments)):
            #print("")
           
            #print("+++++++++"+str(segments[i])+"++++++++++++")
            #print("---------"+str(segments[i+1])+"------------")
            vectorA = segments[i].vector
            vectorB = segments[i+1].vector
            #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #print("+++++++++"+str(vectorA)+"++++++++++++")
            #print("---------"+str(vectorB)+"------------")
            rawvalue = vectorA.cross(vectorB)
            value = utils.clamp(rawvalue, 5)
            #print("Rawvalue = " + str(rawvalue) + "Fixed value = " + str(value))
            #print(rawvalue < 0, value < 0)
            if value < 0:
                isconvex = False
                #break
        #if(isconvex): print("CONVEX")
        #else: print("CONCAVE")
        #print("=========CONCAVITY CHECKING END========")
        return isconvex

    #Might want to try and split this method so that it is not so big and complex
    def electBestSegment(self):
        '''The best segment is the segment that can divide this sector into 2 sectors as equally as possible'''
        print("Electing the best segment for splitting")
        print("Number of segments = " + str(len(self.segments)))
        bestSegment = None
        bestSegments = []
        bestNewSegments = []
        segmentsToSplit = [] #These are the segments that would need to be split in half
        for segment in self.segments:
            print("SEGMENT " + segment.name+"   +++++++++++++++++++++++++++++")
            tempSegments = []
            tempNewSegments = []
            others = []
            for other in self.segments:                
                if other is not segment:
                    print(segment.name + " against------OTHER SEGMENT " + other.name)
                    newsegment = segment.intersectAsRay(other)
                    if newsegment is not None: #segment ray intersects other
                        print("+++++++++++NEW SEGMENT = " + str(newsegment))
                        for other2 in self.segments: #check to see if the new segment intersects with any of the segments
                            print("..............Check segment " + other2.name + " intersects?")
                            intersects = False
                            if newsegment.intersectSegment(other2):
                                print("YES")
                                intersects = True
                                break
                            else: print("NO")
                        if not intersects:              
                            #Now need to check if the new segment is completely inside or outside of the sector
                            #We want to be completely inside the sector
                            if self.pointInsideSector(newsegment.midpoint()):
                                print("New segement is inside sector.....Add it to the list")
                                tempSegments.append(segment)
                                tempNewSegments.append(newsegment)
                                others.append(other)
                                #temp.append(newsegment.vertex2.position)
            #print(str(segment) + " intersect with " + str(len(temp)) + " segments.")
            #We only want segments that intersect 1 other segment
            print(segment.name + "   ---------------TEMP NEW SEGMENTS-------------------  " + str(len(tempNewSegments)))
            if len(tempNewSegments) == 1:
                bestSegments += tempSegments
                bestNewSegments += tempNewSegments
                segmentsToSplit += others
                
        print("")
        print("# BEST SEGMENTS TO CHOOSE FROM Initially= " + str(len(bestSegments)))
        for seg in bestSegments:
            print(seg)
        print("-----------------------------------------")
        #From this list of splitting segments, choose the one that splits the segment as close to the middle as possible.
        values = []
        print("")
        print("Refining choices.............")
        for i in range(len(bestNewSegments)):
            value = bestNewSegments[i].intersectSegmentEndpoints(segmentsToSplit[i])
            if value is not None:
                values.append(abs(value - 0.5))

        print("Values = " + str(values))
        if len(values) > 0:
            bestIndex = values.index(min(values))

            bestNewSegment = bestNewSegments[bestIndex]
            print("best new segment = " + str(bestNewSegment))
            segment1, segment2 = segmentsToSplit[bestIndex].split(bestNewSegment)
            self.segments.append(bestNewSegment)
            self.segments.append(Segment(bestNewSegment.p2, bestNewSegment.p1, True))
            self.segments.append(segment1)
            self.segments.append(segment2)
            self.segments.remove(segmentsToSplit[bestIndex])
            return bestSegments[bestIndex]
        #return bestSegments[bestIndex], bestNewSegments[bestIndex], segmentsToSplit[bestIndex]
        #return [bestNewSegments[bestIndex]]
        #return self.segments

    

    def pointInsideSector(self, point):
        '''point is a Vector2.  Check if a point is inside the sector or outside the sector.  Create a ray that points to the right.  Loop through each segment that makes up this sector and count how many sectors this ray crosses.  If that number is odd, the point is inside the sector.  If even, the point is outside.'''
        xvector = Vector2(1,0)
        ray = Ray(point, xvector)
        num_crossings = 0
        #segments = self.segments + self.segments[0:1]
        for segment in self.segments:
            s = ray.intersectSegment(segment)
            if s is not None:
                if s > 0:
                    num_crossings += 1
                
            #k1 = segments[i]
            #k2 = segments[i+1]
            #p1 = self.vertices[k1].position
            #p2 = self.vertices[k2].position
            #segment = Segment(self.vertices[k1], self.vertices[k2])
            #if ray.intersectSegment(segment):
            #    num_crossings += 1
        print("For point " + str(point) + " # of crossings = " + str(num_crossings))
        if utils.evenValue(num_crossings):
            print("NOT INSIDE SECTOR")
            return False
        print("INSIDE SECTOR")
        return True


            
    
