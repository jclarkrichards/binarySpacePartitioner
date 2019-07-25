import pygame
from constants import *
#from Primitives.vectors import Vector2
from Primitives.segment import Segment
#from Primitives.ray import Ray
#from Primitives.vertex import Vertex
#from copy import deepcopy
import utils
"""A sector is an area that is defined by a list of Segment objects.  We can check to see if this sector is convex or concave"""

"""Use this when doing the BSP step. Does things slightly differently than the Sector above"""
class Sector(object):
    def __init__(self, segments):
        print("----SectorBSP-----")
        self.segments = segments
        #for seg in self.segments:
        #    print(seg)
        #print("")
        #print("")
        #print("_______________Segments in this Sector______________")
        #self.segments = self.sortSegments()
        #for seg in self.segments:
        #    print(seg)
        self.sMatrix = {}

    def getSegmentFromName(self, name):
        '''Given a segment name (all segments have unique names) return the Segment object'''
        for segment in self.segments:
            if segment.name == name:
                return segment
        return None
    """
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
            value = utils.clamp(rawvalue, 2)
            #print("Rawvalue = " + str(rawvalue) + "Fixed value = " + str(value))
            #print(rawvalue < 0, value < 0)
            if value < 0:
                isconvex = False
                #break
        #if(isconvex): print("CONVEX")
        #else: print("CONCAVE")
        #print("=========CONCAVITY CHECKING END========")
        return isconvex
    
    def getValuesFromNameList(self, key, D):
        '''Given a list of segment names, return the list of values form the sMatrix'''
        valuelist = []
        for value in D[key]:
            valuelist.append(self.sMatrix[value][key])
        return valuelist
    """
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
                if 0 < value < 1: #between 0 and 1 (inclusive)
                    if value == 0:
                        if self.sMatrix[otherkey][key] != 1:
                            d[key].append(otherkey)
                    elif value == 1:
                        if self.sMatrix[otherkey][key] != 0:
                            d[key].append(otherkey)
                    else:
                        d[key].append(otherkey)
                        
        #remove empty entries
        #for key in d.keys():
        #    if len(d[key]) == 0:
        #        d.pop(key)
        return d
    """
    def resolveMultipleCrossings(self, D):
        '''Given a dictionary, look at the ones with muliple entries.  '''
        print("RESOLVING MULTIPLE CROSSINGS")
        for key in D.keys():
            if len(D[key]) > 1:
                print(key)
                print(D[key])
                #for i in range(len(D[key])):
                values = self.getValuesFromNameList(key, D)
                print(values)
                if utils.allPositive(values):
                    print("All are positive")
                elif utils.allNegative(values):
                    print("All are negative")
                else:
                    print("Some are positive and some are negative")
    
    
    def removeBlockedSegments(self, D):
        '''Given the dictionary created from the firstpass, find entries with multiple crossings.'''
        Dnew = {}
        for key in D.keys():
            result = utils.minmaxValues(D, key, self.sMatrix)
            Dnew[key] = result
        return Dnew
    
    def removeOutsideSegments(self, D):
        '''Given the dictionary created from firstpass, find the entries that have segments on the outside of the sector'''
        Dnew = {}
        for key in D.keys():
            segment = self.getSegmentFromName(key)
            point = None
            for item in D[key]:
                if self.sMatrix[item][key] > 0:
                    point = segment.p2 + segment.vector * ((self.sMatrix[item][key] - 1) / 2.0)
                elif self.sMatrix[item][key] < 0:
                    point = segment.p1 + segment.vector * (self.sMatrix[item][key] / 2.0)

                #Now use the point to see if it is inside or outside of the sector
                if point is not None:
                    print(key, item)
                    inside = self.pointInsideSector(point)
                    if inside:
                        if key in Dnew.keys():
                            Dnew[key].append(item)
                        else:
                            Dnew[key] = [item]

        return Dnew
    
    def removeMultipleCrossings(self, D):
        Dnew = {}
        for key in D.keys():
            if len(D[key]) == 1:
                Dnew[key] = D[key]
        return Dnew
    """
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
        print(segment.name + " || " + testSegment.name)
        #if (segment.direction == testSegment.direction) or (segment.direction == (testSegment.direction * -1)):
        #    return "right"
        v1 = testSegment.p1 - segment.p1
        v2 = testSegment.p2 - segment.p1
        #print("s.p1 ="+ str(segment.p1) + " s.p2 = " + str(segment.p2))
        #print("t.p1 ="+ str(testSegment.p1) + "t.p2 = " + str(testSegment.p2))
        #print(segment.vector)
        
        #print(str(v1)+" and " + str(v2))
        #print("segment x v1 and segment x v2")
        #print(str(segment.vector.cross(v1)) + " and " + str(segment.vector.cross(v2)))
        #print("")
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
                
        print("value = " + str(value))
        print("")
        if value >= 0:
        #if segment.vector.cross(v1) >=0 and segment.vector.cross(v2) >= 0:
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
    
    def splitSegments(self):
        #Matrices (Dictionaries) for when key intersects with the inner dictionary segments
        print("GETTING THE BEST SEGMENT")
        self.sMatrix = self.getIntersectionMatrix()
        results = self.getSegmentCrossingLists()
        print("FIRST PASS")
        print(results)
        #For each segment, how many segments are to the right and left of this segment?
        divisionMatrix = self.getDivisionMatrix(results)
        print("------------DIVISION MATRIX # SEGEMENTS ON EACH SIDE OF SEGMENT-----------")
        print(divisionMatrix)
        #Using the divisionMatrix, the best segment is the one that divides the sector most evenly.  
        bestName = self.getMostEvenSplit(divisionMatrix)
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
            mainSegment = self.getSegmentFromName(bestName)
            print(self.getSegmentSide(mainSegment, newSegment1))
            print(self.getSegmentSide(mainSegment, newSegment2))
            print("")

        print("____________-------------_________________----------")
        #results = self.removeMultipleCrossings(firstpass)
        #print("Multiple crossings removed")
        #print(results)
        #filteredResults = self.removeBlockedSegments(firstpass)
        #Use the firstpass dictionary to find and remove any outside crossings
        #print("Filtered Results")
        #print(filteredResults)
        #print("")
        #print("")
        #print("Removed outside segments")
        #filteredResults = self.removeOutsideSegments(results)
        
        #print(filteredResults)

        #print("Final Results")
        #print(finalresults)
        #secondpass = self.resolveMultipleCrossings(firstpass)
        #print(secondpass)
        
        
        #print("S Matrix")
        #for key in self.sMatrix.keys():
        #    for otherkey in self.sMatrix[key].keys():
        #        print(key + " intersects " + otherkey + " at " + str(self.sMatrix[key][otherkey]))
        #    print("")

            
    #Might want to try and split this method so that it is not so big and complex
    """
    def electBestSegment(self):
        '''The best segment is the segment that can divide this sector into 2 sectors as equally as possible'''
        print("Electing the best segment for splitting")
        print("Number of segments = " + str(len(self.segments)))
        bestSegment = None
        bestSegments = []
        bestNewSegments = []
        segmentsToSplit = [] #These are the segments that would need to be split in half
        for segment in self.segments:
            print("")
            print("")
            print("")
            print("SEGMENT " + segment.name+"   +++++++++++++++++++++++++++++")
            tempSegments = []
            tempNewSegments = []         
            others = []
            for other in self.segments:                
                if other is not segment:
                    print(segment.name + " against------OTHER SEGMENT " + other.name)
                    s, t = utils.intersect(segment.p1, other.p1, segment.vector, other.vector)

                    newsegment = segment.intersectAsRay(other, includeEndpoints=True)


                    if newsegment is not None: #segment ray intersects other
                        if newsegment not in tempNewSegments: 
                            print("+++++++++++NEW SEGMENT = " + str(newsegment))
                            for other2 in self.segments: #check to see if the new segment intersects with any of the segments
                                print("..............Check segment " + other2.name + " intersects?")
                                intersects = False
                                if newsegment.intersectSegment(other2, includeEndpoints=True):
                                    print("YES")
                                    intersects = True
                                    break
                                else: print("NO")
                            if not intersects:              
                                #Now need to check if the new segment is completely inside or outside of the sector
                                #We want to be completely inside the sector
                                if self.pointInsideSector(newsegment.midpoint()):
                                    print("New segement is inside sector.....Add it to the list")
                                    tempSegments.append(segment) #segment I am testing
                                    tempNewSegments.append(newsegment)  #extension from segment to other
                                    others.append(other) #segment that the newsegment crosses
                                
            #print(str(segment) + " intersect with " + str(len(temp)) + " segments.")
            #We only want segments that intersect 1 other segment
            print(segment.name + "   ---------------TEMP NEW SEGMENTS-------------------  " + str(len(tempNewSegments)))
            if len(tempNewSegments) == 1:
                bestSegments += tempSegments
                bestNewSegments += tempNewSegments
                segmentsToSplit += others
            else:
                print(segment.name + " splits sector into more than 2 sectors, so discard.")
            #break #testing
                
        #print("")
        print("# BEST SEGMENTS TO CHOOSE FROM Initially= " + str(len(bestSegments)))
        for seg in bestSegments:
            print(seg)
        print("-----------------------------------------")
        #From this list of splitting segments, choose the one that splits the segment as close to the middle as possible.
        values = []
        print("")
        print("Refining choices.............")
        for i in range(len(bestNewSegments)):
            t = bestNewSegments[i].getOtherIntersectionValue(segmentsToSplit[i], includeEndpoints=True)
            if t is not None:
                print(str(t) + " ,,,,,,,,,")
                values.append(utils.clamp(abs(t - 0.5), 2))

        #print("Values = " + str(values))
        if len(values) > 0:
            bestIndex = values.index(min(values))

            bestNewSegment = bestNewSegments[bestIndex]
            #print("best new segment = " + str(bestNewSegment))
            segment2 = segmentsToSplit[bestIndex].split(bestNewSegment)
            self.segments.append(bestNewSegment)
            self.segments.append(bestNewSegment.reverse())
            #self.segments.append(Segment(bestNewSegment.p2, bestNewSegment.p1, True))
            #self.segments.append(segment1)
            self.segments.append(segment2)
            #self.segments.remove(segmentsToSplit[bestIndex])
            
            return bestSegments[bestIndex]
        #return bestSegments[bestIndex], bestNewSegments[bestIndex], segmentsToSplit[bestIndex]
        #return [bestNewSegments[bestIndex]]
        #return self.segments

    
    """
    """
    def pointInsideSector(self, point):
        '''point is a Vector2.  Check if a point is inside the sector or outside the sector.  Create a ray that points to the right.  Loop through each segment that makes up this sector and count how many sectors this ray crosses.  If that number is odd, the point is inside the sector.  If even, the point is outside.'''
        #print("IS THIS POINT INSIDE THE SECTOR???")
        #print("------------------- " + str(point) + " -------------------------")
        xvector = Vector2(1,0)
        ray = Ray(point, xvector)
        num_crossings = 0
        #print("Num segments to check: " + str(len(self.segments)))
        for segment in self.segments:
            #print("Checking segment " + segment.name)
            t = ray.intersectSegmentRaw(segment)
            #print("t = " + str(t))
            if t is not None:
                if 0 < t < 1:
                    #print("Crossing a line normally")
                    num_crossings += 1
                elif t == 0: #we are crossing the segments p1 vector.  check if p2 is above us
                    #print("CROSSING " + segment.name + " p1")
                    if segment.p2.y < segment.p1.y:
                        #print(segment.name + " p2 is above p1")
                        num_crossings += 1
                elif t == 1: #we are crossing the segments p2 vector.  check if p1 is above us
                    #print("CROSSING " + segment.name + " p2")
                    if segment.p1.y < segment.p2.y:
                        #print(segment.name + " p1 is above p2")
                        num_crossings += 1

        #print("For point " + str(point) + " # of crossings = " + str(num_crossings))
        if utils.evenValue(num_crossings):
            #print("NOT INSIDE SECTOR")
            return False
        #print("INSIDE SECTOR")
        return True
    """

            
    
