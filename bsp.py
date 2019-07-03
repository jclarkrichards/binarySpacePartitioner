import pygame
from Primitives.btree import BinaryTree
from Primitives.sector import SectorBSP

"""Input a list of SegmentDirected objects"""
class BinarySpacePartitioner(object):
    def __init__(self, segments):
        self.segments = segments
        self.tree = BinaryTree() #empty tree
        self.sector = None
        
    def createTree(self):
        '''Initially add all the segments to the root node.'''
        for segment in self.segments:
            self.tree.addSegment(segment)
        isconvex = self.convexSectorCheck()
        if not isconvex:
            bestsector = self.getBestSector()
        return bestsector #should not return, just for testing
            
    def convexSectorCheck(self):
        '''Check if a group of segments defines a convex or concave area'''
        segmentList = self.tree.pointer.data
        #print(segmentList)
        self.sector = SectorBSP(segmentList)
        isconvex = self.sector.convexOrConcave()
        return isconvex

    def getBestSector(self):
        #elect a segment from the segmentList to remain on the node.  Then move the other segments down to the child nodes depending on left or right status.
        testVertexList = self.sector.electBestSegment()
        #print("Num of lskdjafjdlsf = " + str(len(testVertexList)))
        return testVertexList #just for testing
