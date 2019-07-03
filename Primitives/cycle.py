from copy import deepcopy
"""A Cycle is a list of values where the order of the list matters.  It is assumed that the last element in the list connects to the first element in the list.  Ex) [1,2,3,4,5] is assumed to mean 1 connects to 2 and 5.  2 connects to 1 and 3, and so on.  Also [1,2,3,4,5] == [5,4,3,2,1] == [2,3,4,5,1] == [4,5,1,2,3] == etc."""
class Cycle(object):
    def __init__(self, sequence):
        self.sequence = sequence

    def __str__(self):
        '''For [1,2,3,4] returns [1,2,3,4,1]'''
        result = self.sequence + [self.sequence[0]]
        return str(result)

    def __eq__(self, other):
        combos = self.allCycleCombos(self.sequence)
        if other in combos:
            return True
        return False

    def __hash__(self):
        return id(self)

    def allCycleCombos(self, cycle):
        '''Given a cycle like [1,2,3,4], return all combos such as [4,3,2,1] and [3,4,1,2]'''
        combos = [cycle]
        temp_reverse = deepcopy(cycle)
        temp_reverse.reverse()
        combos.append(temp_reverse)
        for i in range(len(cycle)-1):
            temp = cycle[i+1:] + cycle[0:i+1]
            combos.append(temp)
            temp_reverse = deepcopy(temp)
            temp_reverse.reverse()
            combos.append(temp_reverse)
        return combos
