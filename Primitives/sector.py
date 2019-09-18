import pygame
from constants import *
from Primitives.segment import Segment
import utils
"""A sector is an area that is defined by a list of Segment objects.  We can check to see if this sector is convex or concave"""

"""Use this when doing the BSP step. Does things slightly differently than the Sector above"""
class Sector(object):
    def __init__(self, segments):
        print("----SectorBSP-----")
        self.segments = segments
        self.bestSegment = None
        self.sMatrix = {}

    def getSegmentFromName(self, name):
        '''Given a segment name (all segments have unique names) return the Segment object'''
        for segment in self.segments:
            if segment.name == name:
                return segment
        return None
    
    def getIntersectionMatrix(self):
        '''Get the sMatrix which shows how all of the segments intersect each other'''
        sMatrix = {}  #Value for key segment to intersect the other segments
        for segment in self.segments:
            sMatrix[segment.name] = {}
            for other in self.segments:
                if other is not segment:
                    s, t = utils.intersect(segment.p1, other.p1, segment.vector, other.vector)
                    sMatrix[segment.name][other.name] = t;
        return sMatrix

    def getSegmentCrossingLists(self):
        '''Using the sMatrix, return a dictionary of segments and the segments that they would actually cross if extended'''
        d = {}
        for key in self.sMatrix.keys():
            d[key] = []
            for otherkey in self.sMatrix[key].keys():
                value = self.sMatrix[key][otherkey]
                print(key, otherkey, len(self.sMatrix))
                print(self.sMatrix)
                if value is not None:
                    if 0 < value < 1: #between 0 and 1 (inclusive)
                        if value == 0:
                            if self.sMatrix[otherkey][key] != 1:
                                d[key].append(otherkey)
                        elif value == 1:
                            if self.sMatrix[otherkey][key] != 0:
                                d[key].append(otherkey)
                        else:
                            d[key].append(otherkey)
                        
        return d
    
    def getDivisionMatrix(self, D):
        '''Given a dictionary found after calling getSegmentCrossingLists.  Find how many segments are to the left and right of each key'''
        DM = {}
        for key in D.keys():
            DM[key] = {"left":0, "right":0}
            for item in D[key]: #We already know key intersects these segments, so add to both left and right
                DM[key]["left"] += 1
                DM[key]["right"] += 1
            for item in self.sMatrix.keys():
                if item is not key and item not in D[key]: #For all of the other segments though, they should be entirely to left or right
                    segment = self.getSegmentFromName(key)
                    testSegment = self.getSegmentFromName(item)
                    leftOrRight = self.getSegmentSide(segment, testSegment)
                    #print(key +" and " + item + " : " + leftOrRight)
                    DM[key][leftOrRight] += 1
                
        return DM

    def getSegmentSide(self, segment, testSegment):
        '''Which side of segment does testSegment lie on?  left or right?  If testSegment is on same line as segment, then it is on the right.'''
        v1 = testSegment.p1 - segment.p1
        v2 = testSegment.p2 - segment.p1
        value1 = segment.vector.cross(v1)
        value2 = segment.vector.cross(v2)
        if (value1 > 0 and value2 < 0) or (value1 < 0 and value2 > 0):
            vals = [abs(value1), abs(value2)]
            index = vals.index(max(vals))
            if index == 0:
                value = value1
            else:
                value = value2
        else:
            if value1 >= 0 and value2 >= 0:
                value = max([value1, value2])
            else:
                value = min([value1, value2])

        if value >= 0:
            return "right"
        return "left"
        
    def getMostEvenSplit(self, DM):
        '''The division matrix has left and right.  We subtract the 2 and return the segment with the lowest value'''
        D = {}
        for key in DM.keys():
            D[key] = abs(DM[key]["left"] - DM[key]["right"])
        minval = min(D.values())
        for key in D.keys():
            if D[key] == minval:
                return key
        return None

    def checkSplittableSegmentExists(self, DM):
        '''Use the division matrix to check if there is at least 1 splittable segment'''
        for key in DM.keys():
            if DM[key]["left"] > 0 and DM[key]["right"] > 0:
                return True
        print("NO SPLITTABLE SEGMENTS")
        return False
                
    def splitSegments(self):
        #Matrices (Dictionaries) for when key intersects with the inner dictionary segments
        print("GETTING THE BEST SEGMENT")
        print("Number of segments = " + str(len(self.segments)))
        self.sMatrix = self.getIntersectionMatrix()
        results = self.getSegmentCrossingLists()
        print("FIRST PASS")
        print(results)
        #For each segment, how many segments are to the right and left of this segment?
        divisionMatrix = self.getDivisionMatrix(results)
        print("------------DIVISION MATRIX # SEGEMENTS ON EACH SIDE OF SEGMENT-----------")
        print(divisionMatrix)
        #Using the divisionMatrix, the best segment is the one that divides the sector most evenly.
        hasSplittableSegment = self.checkSplittableSegmentExists(divisionMatrix)
        if hasSplittableSegment:
            bestName = self.getMostEvenSplit(divisionMatrix)
            self.bestSegment = self.getSegmentFromName(bestName)
            print("Best segment to use for the split is ............. " + bestName)
            #return bestName
            #We now have the bestest segment to use to split this sector in two or more
            #Use this sector, the divisionMatrix, and the values in the sMatrix to split the segments that it intersects into 2 segments
            #self.splitSegments(bestName, divisionMatrix[bestName])
            for item in results[bestName]:
                mult = self.sMatrix[bestName][item]
                print("split " + item + " at " + str(mult))
                segment = self.getSegmentFromName(item)
                point = segment.p1 + segment.vector * mult
                newSegment1 = Segment(segment.p1, point, name=segment.name)
                newSegment2 = Segment(point, segment.p2, name=segment.name+"#")
                self.segments.remove(segment)
                self.segments.append(newSegment1)
                self.segments.append(newSegment2)
                print("SANITY CHECK")
                #mainSegment = self.getSegmentFromName(bestName)
                print(self.getSegmentSide(self.bestSegment, newSegment1))
                print(self.getSegmentSide(self.bestSegment, newSegment2))
                print("")
        print("soooooo #of segments = " + str(len(self.segments)))

        print("____________-------------_________________----------")
            

            
    
