import pygame
import utils
from Primitives.vectors import Vector2
from Primitives.cycle import Cycle
from copy import deepcopy

"""The class takes in the vertices dictionary and a list of tuples of 2 elements each.  The number of base cycles will be exactly the same number of elements in the segments list."""
class BaseSectors(object):
    def __init__(self, vertices, segments, graph):
        self.vertices = deepcopy(vertices)
        self.segments = segments
        self.graph = graph
        self.cycles = [] #A list of Cycle objects
        self.perimeter = self.findPerimeter()
        self.findAllBaseSectors()
        
    def findAllBaseSectors(self):
        '''We have a list of starting segments.  Start on each edge and traverse the graph CW and CCW until we reach our starting edge.  Then just get a unique list of these lists to find the base cycles'''
        for pair in self.segments:
            cycleCW = self.findCycle(pair, "CW")
            cycleCCW = self.findCycle(pair, "CCW")
            self.addCycle(cycleCW)
            self.addCycle(cycleCCW)

        #print("========There are " + str(len(self.cycles)) + " sectors===========")
        #for sector in self.cycles:
        #    print(sector)
        #print("")
        #print("")
            
    def findCycle(self, pair, direction="CW"):
        '''Given a pair of vertex keys, find the cycle that travels either CW or CCW'''
        prevertex, vertex = pair 
        end = deepcopy(prevertex)
        tempSequence = [vertex]
        
        while vertex != end:
            basevector = self.vectorFromVertices(prevertex, vertex)
            angles = self.getAngles(vertex, basevector, prevertex)
            crosses = self.getCrossProducts(vertex, basevector, prevertex)
            if direction == "CW":
                nextvertex = self.nextVertexCW(angles, crosses)
            else:
                nextvertex = self.nextVertexCCW(angles, crosses)
                
            tempSequence.append(nextvertex)
            prevertex = vertex
            vertex = nextvertex

        tempCycle = Cycle(tempSequence)
        return tempCycle

    def addCycle(self, cycle):
        '''Add a valid cycle to the list of cycles.  cycle is a Cycle object'''
        if cycle not in self.cycles:
            if not cycle == self.perimeter:
                #print("Adding cycle " + str(cycle))
                self.cycles.append(cycle)
        

    def getAngles(self, vertex, vector, ignorevertex=None):
        '''Get all the angles between the vector and the other vectors that point from vertex to the neighbors except for the ignorevertex'''
        angles = {}
        for v in self.vertices[vertex].neighbors:
            if ignorevertex is not None:
                if v.key != ignorevertex:
                    thisvector = self.vectorFromVertices(v.key, vertex)
                    angles[v.key] = vector.angle(thisvector)
            else:
                thisvector = self.vectorFromVertices(v.key, vertex)
                angles[v.key] = vector.angle(thisvector)
        return angles

    def getCrossProducts(self, vertex, vector, ignorevertex=None):
        '''Get all the cross products between the vector and the other vectors that point from vertex to the neighbors except for the ignorevertex'''
        crosses = {}
        for v in self.vertices[vertex].neighbors:
            if ignorevertex is not None:
                if v.key != ignorevertex:
                    thisvector = self.vectorFromVertices(v.key, vertex)
                    crosses[v.key] = vector.cross(thisvector)
            else:
                thisvector = self.vectorFromVertices(v.key, vertex)
                crosses[v.key] = vector.cross(thisvector)
        return crosses

    def vectorFromVertices(self, vertex1, vertex2):
        '''Return a vector that points from vertex2 to vertex1'''
        return self.vertices[vertex1].position - self.vertices[vertex2].position
  
    def nextVertexCCW(self, angles, crosses):
        '''Given a dictionary of vertices as keys and [cross, angle] as values, first find all vertices with positive crosses.  For those return the vertex with the smallest angle.  If all crosses are negative, then return the vertex with the largest angle'''
        positives, negatives = self.splitDictionary(crosses)
        if len(positives) > 0:
            angles = utils.removeKeys(angles, negatives)
            vertex = self.smallestAngle(angles, positives)
        else:
            vertex = self.largestAngle(angles, negatives)
        return vertex

    def nextVertexCW(self, angles, crosses):
        '''Given a dictionary of vertices as keys and [cross, angle] as values, first find all vertices with negative crosses.  For those return the vertex with the smallest angle.  If all crosses are positive, then return the vertex with the largest angle'''
        positives, negatives = self.splitDictionary(crosses)
        if len(negatives) > 0:
            angles = utils.removeKeys(angles, positives)
            vertex = self.smallestAngle(angles, negatives)
        else:
            vertex = self.largestAngle(angles, positives)
        return vertex

    def smallestAngle(self, angles, keys):
        '''Given a list of keys, look through the dictionary and return the key with the smallest angle.'''
        return min(angles, key=lambda key: angles[key])
        
    def largestAngle(self, angles, keys):
        '''Given a list of keys, look through the dictionary and return the key with the largest angle.'''
        return max(angles, key=lambda key: angles[key])
    
    def splitDictionary(self, d):
        '''Given a dictionary with values, return two lists of keys that correspond to positive and negative values in the dictionary.'''
        positives = [k for k in d.keys() if d[k] >= 0]
        negatives = [k for k in d.keys() if d[k] < 0]
        return positives, negatives

    def findPerimeter(self):
        '''From the dictionary of vertices, find the perimeter by finding the left most vertex and traveling CW.'''
        print("Finding the perimeter")
        vertex = min(self.vertices, key=lambda key: self.vertices[key].position.x)
        print("left most vertex is " + str(vertex))
        basevector = Vector2(-1,0)
        angles = self.getAngles(vertex, basevector)
        crosses = self.getCrossProducts(vertex, basevector)
        nextvertex = self.nextVertexCW(angles, crosses)
        initialPair = [vertex, nextvertex]
        print("Initial perimeter pair = " + str(initialPair))
	return self.findCycle(initialPair, "CW")

        

            
