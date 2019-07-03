class Stack(object):
    def __init__(self):
        self.items = []

    def length(self):
        return len(self.items)

    def isEmpty(self):
        if self.length() > 0:
            return False
        return True

    def clear(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.length() > 0:
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None

    def peek(self):
        if self.length() > 0:
            return self.items[self.length()-1]
        return None
