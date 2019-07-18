import pygame
from btree import BinaryTree

"""Input a list of SegmentDirected objects"""
class BinarySpacePartitioner(object):
    def __init__(self):
        self.createTree()
        
    def createTree(self):
        '''Initially add all the segments to the root node.'''
        self.tree = BinaryTree()
        self.tree.addData(3)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoLeft()
        self.tree.addData(5)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoRight()
        self.tree.addData(12)
        self.tree.gotoParent()
        self.tree.gotoLeft()
        self.tree.addData(10)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoLeft()
        self.tree.addData(11)
        self.tree.gotoParent()
        self.tree.gotoRight()
        self.tree.addData(13)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoLeft()
        self.tree.addData(18)
        #self.tree.pointer.isConvex = False
        self.tree.gotoParent()
        self.tree.gotoRight()
        self.tree.addData(23)
        self.tree.gotoRoot()
        self.tree.gotoRight()
        self.tree.addData(2)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoRight()
        self.tree.addData(23)
        self.tree.gotoParent()
        self.tree.gotoLeft()
        self.tree.addData(4)
        self.tree.addLeft()
        self.tree.addRight()
        self.tree.gotoLeft()
        self.tree.addData(34)
        self.tree.gotoParent()
        self.tree.gotoRight()
        self.tree.addData(1)
        self.tree.addRight()
        self.tree.gotoRight()
        self.tree.addData(78)
        
        
    def traverseTree(self):
        '''Traverse down the tree until you get to a leaf that is concave.  We are done traversing the tree when all of the leafs are convex.'''
        self.tree.gotoRoot() #start at the root node whenever we traverse the tree
        self.findLeaf()
        print("Finished traversing the TREE")
        print(self.tree.pointer.data)

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
        self.tree.gotoLeft()
        self.findLeaf()

    def traverseRight(self):
        '''go to the right node'''
        self.tree.gotoRight()
        self.findLeaf()

    def traverseToParent(self):
        '''Go back to the parent'''
        self.tree.pointer.visited = True
        self.tree.gotoParent()
        self.findLeaf()
    
    def findLeaf(self):
        if self.tree.isleaf():
            print(self.tree.pointer.data)
            if self.tree.pointer.isConvex:
                self.traverseToParent()
            else:
                print("found our concave leaf")        
        else:
            if self.canTraverseLeft():
                self.traverseLeft()
            elif self.canTraverseRight():
                self.traverseRight()
            elif self.canTraverseToParent():
                self.traverseToParent()
            else:
                print("Finished, All are convex")

    
bsp = BinarySpacePartitioner()
bsp.traverseTree()
            



