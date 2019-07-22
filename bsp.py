import pygame
import utils
from Primitives.btree import BinaryTree
from Primitives.sector import Sector

"""Input a list of SegmentDirected objects"""
class BinarySpacePartitioner(object):
    def __init__(self, segments):
        #print("TIME FOR SOME BSP")
        self.segments = segments
        self.segmentList = segments
        self.tree = BinaryTree() #empty tree
        self.sector = None
        #print(type(self.segments))
        #print("Number of initial segments = " + str(len(self.segments)))
        
    def createTree(self):
        '''Initially add all the segments to the root node.'''
        self.tree.pointer.data = self.segments
        #for segment in self.segments:
        #    self.tree.addSegment(segment)
        self.sectorCheck(self.tree.pointer)
        #self.traverseTree()
        
    def traverseTree(self):
        '''Traverse down the tree until you get to a leaf that is concave.  We are done traversing the tree when all of the leafs are convex.'''
        print("")
        print("")
        print("")
        print("Traverse Tree")
        self.tree.gotoRoot() #start at the root node whenever we traverse the tree
        self.findLeaf()
        #if self.tree.pointer is not self.tree.root:
        #    self.sectorCheck()

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
            if self.tree.pointer.isConvex:
                self.traverseToParent()
            else:
                print("----------CONCAVE LEAF---------")
                self.getBestSegment()
                #self.sectorCheck()
        else:
            if self.canTraverseLeft():
                self.traverseLeft()
            elif self.canTraverseRight():
                self.traverseRight()
            elif self.canTraverseToParent():
		self.traverseToParent()
            else:
                print("Finished... All are convex")            
    
    def sectorCheck(self, treenode):
        '''Pointing at some data, check if data represents a convex or concave sector'''
        print("CHECKING THE SECTOR FOR CONCAVITY")
        segments = treenode.data
        self.sector = Sector(segments)
        isconvex = self.sector.convexOrConcave()
        print("# segments = " + str(len(segments)))
        print("Is convex = " + str(isconvex))
        treenode.isConvex = isconvex
            
    def convexSectorCheck(self, segments):
        '''Check if a group of segments defines a convex or concave area'''
        #segmentList = self.tree.pointer.data
        #print(segmentList)
        self.sector = Sector(segments)
        isconvex = self.sector.convexOrConcave()
        return isconvex

    def getBestSegment(self):
        '''elect a segment from the segmentList to remain on the node.  Then move the other segments down to the child nodes depending on left or right status.'''
        print("++++++++++++++++++++Getting the best segment++++++++++++++")
        segments = self.tree.pointer.data
        print("Number of segments : " + str(len(segments)))
        sector = Sector(segments)
        bestSegment = sector.electBestSegment()
        print("Best segment is " + str(bestSegment))
        self.segments = sector.segments
        print("Segments as they are now:::")
        for seg in self.segments:
            print(seg)
        print("................,,,,,.....,,,,,,.................")
        print("")
   
        self.segmentList += self.segments #Only for display purposes so I can see all the segments even if duplicates.

        """Next we need to check to see if these segments get divided up corretly into the tree."""


        #self.tree.pointer.data = [bestSegment]
        #self.divideSegments(bestSegment, self.segments)



        #print("Segment = " + str(segment))
        #print("New Segment = " + str(newSegment))
        #print("Split Segment = " + str(splitSegment))
        #print("Num of lskdjafjdlsf = " + str(len(testVertexList)))
        #return testVertexList #just for testing
        #print("Number of Segments = " + str(len(self.segments)))

        
    def divideSegments(self, mainSegment, segments):
        '''Divide the segments into the left and right child nodes.  Create the left and right nodes for the node the tree pointer is pointing to and put the segments there depending if they are left or right of the mainSegment.  Then in the end we call the traverseTree in order to start the process over again.'''
        print("DIVIDING THE SEGMENTS")
        print(str(len(segments)) + " to divide up into LEFT and RIGHT")
        #print(mainSegment)
        #print("---------------------")
        for segment in segments:
            #print(segment)
            rightside = utils.vectorOnRight(mainSegment, segment)
            leftside = utils.vectorOnLeft(mainSegment, segment)
            #print("Pointing to: " + str(self.tree.pointer))
            if rightside and not leftside:
                print("Segment is on the right------------>")
                self.tree.addSegmentRight(segment)
            elif leftside and not rightside:
                print("<--------------Segment is on the left")
                self.tree.addSegmentLeft(segment)
            elif not rightside and not leftside:
                if utils.sameDirection(mainSegment, segment):
                    print("On same line... go to the right------------------>")
                    self.tree.addSegmentRight(segment)
                else:
                    self.tree.addSegmentLeft(segment)
                    print("<----------------On same line... go to the left")
            #else:
            #    print("well then what the fuck happened?")
        #print("---------------------------------------")
        #print("")
        self.sectorCheck(self.tree.pointer.left)
        self.sectorCheck(self.tree.pointer.right)
        #self.traverseTree()
    
