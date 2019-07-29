
"""This is the class for a binary tree.  Every node in a binary tree only has 2 branches: a left branch and a right branch.  """
"""This TreeNode is a node that has a value and 2 children as the branches.  The data in the node is a SegmentDirected object.  Initially, the data can be a list of SegmentDirected objects.  Then one of those segments gets elected and becomes the only member of the data.  The rest of the segments then go to the left and right branches.  A virtual segment is a segment that is not really there (or was not originally).  It is an invisible segment that still needs to exist in order to define the sector that the data represents when it is a list"""
class TreeNode(object):
    def __init__(self):
        self.data = []
        self.virtual = False 
        self.left = None
        self.right = None
        self.parent = None
        #self.isConvex = False
        self.visited = False

    def printData(self):
        if type(self.data) is list:
            for d in self.data:
                print(d)
        else:
            print(self.data)
                

    
class BinaryTree(object):
    def __init__(self):
        self.root = TreeNode()
        self.pointer = self.root

    def setSegment(self, segment):
        '''Whatever is already in the data gets wiped and replaced by this'''
        self.pointer.data = segment
        
    def addSegment(self, segment):
        '''Add a segment to the node that is being pointed at currently.'''
        self.pointer.data.append(segment)

    def addSegmentLeft(self, segment):
        '''Add the segment to the left child of node the pointer is pointing to.  Create child if it does not exist.'''
        self.addLeft()
        self.pointer.left.data.append(segment)
        
    def addSegmentRight(self, segment):
        '''Add the segment to the right child of node the pointer is pointing to.  Create child if it does not exist.'''
        self.addRight()
        self.pointer.right.data.append(segment)
    
    def addData(self, data):
        self.pointer.data.append(data)
        
    def addLeft(self):
        '''Add a TreeNode object to the TreeNode being pointed at currently'''
        if self.pointer.left is None:
            self.pointer.left = TreeNode()
            self.pointer.left.parent = self.pointer

    def addRight(self):
        '''Add a TreeNode object to the TreeNode being pointed at currently'''
        if self.pointer.right is None:
            self.pointer.right = TreeNode()
            self.pointer.right.parent = self.pointer

    def gotoRight(self):
        '''Move the pointer to point to the right branch of current Node if it exists'''
        if self.pointer.right is not None:
            self.pointer = self.pointer.right

    def gotoLeft(self):
        '''Move the pointer to point to the left branch of the current Node if it exists'''
        if self.pointer.left is not None:
            self.pointer = self.pointer.left

    def gotoParent(self):
        '''Wherever the pointer is, move it up to the parent Node if it exists'''
        if self.pointer.parent is not None:
            self.pointer = self.pointer.parent

    def gotoRoot(self):
        '''Go all the way up to the root node'''
        self.pointer = self.root
    
    def isleaf(self):
        '''Check if the node the pointer is pointing to is a leaf or not'''
        if self.pointer.left is None and self.pointer.right is None:
            return True
        return False
    
