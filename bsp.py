import pygame
import utils
from Primitives.btree import BinaryTree
from Primitives.sector import Sector

"""Input a list of SegmentDirected objects"""
class BinarySpacePartitioner(object):
    def __init__(self, segments):
        self.segments = segments
        self.segmentList = segments
        self.tree = BinaryTree() #empty tree
        self.sector = None
        #self.player = None
        
    def createTree(self):
        '''Initially add all the segments to the root node.'''
        self.tree.pointer.data = self.segments
        
    def traverseTree(self):
        '''Traverse down the tree until you get to a leaf that is concave.  We are done traversing the tree when all of the leafs are convex.'''
        print("")
        print("")
        print("")
        print("Traverse Tree")
        self.tree.gotoRoot() #start at the root node whenever we traverse the tree
        self.findLeaf()

    def canTraverseLeft(self):
        '''Check if able to move to the left child node'''
        if self.tree.pointer.left is not None:
            if not self.tree.pointer.left.visited:
                return True
        return False

    def canTraverseRight(self):
        '''Check if able to move to the right child node'''
        if self.tree.pointer.right is not None:
            if not self.tree.pointer.right.visited:
                return True
        return False

    def canTraverseToParent(self):
        if self.tree.pointer.parent is not None:
            return True
        return False
    
    def traverseLeft(self):
        '''go to the left node'''
        print("<----LEFT")
        self.tree.gotoLeft()
        self.findLeaf()

    def traverseRight(self):
        '''go to the right node'''
        print("RIGHT---->")
        self.tree.gotoRight()
        self.findLeaf()

    def traverseToParent(self):
        '''Go back to the parent'''
        print("^^^PARENT^^^")
        self.tree.pointer.visited = True
        self.tree.gotoParent()
        self.findLeaf()

    def findLeaf(self):
        if self.tree.isleaf():
            #if self.tree.pointer.isConvex:
            #    self.traverseToParent()
            #else:
            print("----------LEAF FOUND---------")
            for seg in self.tree.pointer.data:
                print(seg)
            print("")
            print("")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("")
            print("")
            sector = self.getBestSegment()
            print("# segments is " + str(len(sector.segments)))
            if sector.bestSegment is not None:
                self.divideSegments(sector)
            else:
                print("No segments selected for splitting")
                if self.canTraverseToParent():
                    self.traverseToParent()
            
        else:
            if self.canTraverseLeft():
                self.traverseLeft()
            elif self.canTraverseRight():
                self.traverseRight()
            elif self.canTraverseToParent():
		self.traverseToParent()
            else:
                print("Finished... All are convex")            

    def getBestSegment(self):
        '''elect a segment from the segmentList to remain on the node.  Then move the other segments down to the child nodes depending on left or right status.'''
        print("++++++++++++++++++++Getting the best segment++++++++++++++")
        segments = self.tree.pointer.data
        print("Number of segments : " + str(len(segments)))
        sector = Sector(segments)
        sector.splitSegments()
        #print("Immediately after sector.splitSegment... # segments = " + str(len(sector.segments)))
        return sector

    def divideSegments(self, sector):
        '''Divide the segments from the sector into left and right children.  At this point we should be on the correct tree node.'''  
        print("DIVDING THE SEGMENTS")
        print("Segments currently on this node")
        print("Number of segments = " + str(len(sector.segments)))
        print("Number of segments = " + str(len(self.tree.pointer.data)))
        #for seg in self.tree.pointer.data:
        #    print(seg)

        print("-------------------------------------------------------")
        #print("Segments we need to divide into left and right children")
        #for seg in sector.segments:
        #    print(seg)

        #print("The splitting segment is " + sector.bestSegment.name)
        self.tree.setSegment(sector.bestSegment)
        
        for segment in sector.segments:
            if sector.bestSegment.name != segment.name:
                leftOrRight = sector.getSegmentSide(sector.bestSegment, segment)
                print(sector.bestSegment.name +" ::: " + segment.name + " " + leftOrRight)
                if leftOrRight is "right":
                    self.tree.addSegmentRight(segment)
                elif leftOrRight is "left":
                    self.tree.addSegmentLeft(segment)

        print("=====================PARENT===========================")
        #self.tree.gotoParent()
        self.tree.pointer.printData()
        self.tree.gotoLeft()
        print("=====================LEFT===========================")
        self.tree.pointer.printData()
        self.tree.gotoParent()
        self.tree.gotoRight()
        print("=====================RIGHT===========================")
        self.tree.pointer.printData()

        

            
