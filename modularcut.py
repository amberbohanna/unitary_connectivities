# Class definition for Modular Cut

from itertools import combinations, product
from helper import powerset
import networkx as nx

from functions import Connectivity

# Class for Modular Cut, holds onto info re enumeration
class ModularCut:
    def __init__(self, basis, connectivity):
        self.basis = frozenset(basis)
        self.groundset = frozenset(connectivity.groundset)
        self.subsets = frozenset(connectivity.subsets)
        self.connectivity = connectivity
        self.cut = self.populateCut()
        self.graph = self.cutGraph()

    def populateCut(self):
        def iterate(basis, pairs):
            cut = basis
            for b in basis:
                if type(b) is int:
                    b = set([b])
                for s in self.subsets:
                    if b <= s:
                        cut = cut | b
                for (p0, p1) in pairs:
                    if self.connectivity.modular(p0, p1):
                        cut = cut | (p0 & p1)
            return cut

        pairs = combinations(self.subsets, 2)
        cut0 = self.basis
        cut1 = iterate(cut0, pairs)
        while (cut0 != cut1):
            cut0 = iterate(cut1, pairs)
            cut1 = iterate(cut0, pairs)
        return cut0

    def isElision(self):
        for sub in self.subsets:
            if not ((sub in self.cut) or
                    ((self.groundset - sub) in self.cut)):
                return False
        return True

    def isUnitary(self):
        for e in self.groundset:
            if not ((self.groundset - set([e])) in self.cut):
                return False
        return True

    def isConnected(self):
        return not (set() in self.cut)
    
    def cutGraph(self):
#        G = self.connectivity.inclusionGraph.copy()
        G = nx.DiGraph()
        # Encode the cut structure
        for s in self.subsets:
            c = (self.groundset - s)
            if s in self.cut and c in self.cut:
                G.add_edge(s, "x")
                G.add_edge("x", s)
            if s in self.cut and (not (c in self.cut)):
                G.add_edge(s, "x")
            if (not (s in self.cut)) and (c in self.cut):
                G.add_edge("x", s)
            if (not (s in self.cut)) and (not (c in self.cut)):
                G.add_node(s)
                G.add_node(c)
        
        return G
    
# Takes a Connectivity and a ModularCut, adds a new element to the ground
# set and extends the mapping
def modularCutExtension(modcut, connectivity):
    oldmapping = connectivity.mapping
    newelement = len(connectivity.groundset)
    newground = set(range(newelement + 1))
    
    subsets = [frozenset(s) for s in powerset(connectivity.groundset)]
    newmapping = {}
    for s in subsets:
        if s in modcut.cut:
            newmapping[frozenset(s | set([newelement]))] = \
                oldmapping[frozenset(s)]
        else:
            newmapping[frozenset(s | set([newelement]))] = \
                oldmapping[frozenset(s)] + 1
            
        if (connectivity.groundset - s) in modcut.cut:
            newmapping[frozenset(s)] = oldmapping[s]
        else:
            newmapping[frozenset(s)] = oldmapping[s] + 1

    return Connectivity(newmapping, newground)

# Some functions for producing modular cuts
# The cut with the most elements
def maximalCut(connectivity):
    return modularCut(frozenset([frozenset()]), connectivity)

# The cut with the fewest elements
def minimalCut(connectivity):
    return modularCut(frozenset([connectivity.groundset]), connectivity)

# Finds the modular cut corresponding to the flats of the polymatroid
def flatsCut(connectivity):
    polymatroid = connectivityPolymatroid(connectivity)
    return modularCut(polymatroid.flats, connectivity)

def flatsAndComplementsCut(connectivity):
    polymatroid = connectivityPolymatroid(connectivity)
    antiflats = frozenset(
        [polymatroid.groundset - f for f in polymatroid.flats])
    return modularCut(polymatroid.flats | antiflats, connectivity)

# Finds the modular cut corresponding to the nonflats of the polymatroid
def nonFlatsCut(connectivity):
    polymatroid = connectivityPolymatroid(connectivity)
    return modularCut(polymatroid.nonflats, connectivity)

def nonFlatsAndComplementsCut(connectivity):
    polymatroid = connectivityPolymatroid(connectivity)
    antinonflats = frozenset(
        [polymatroid.groundset - n for n in polymatroid.nonflats])
    return modularCut(polymatroid.nonflats | antinonflats, connectivity)

# Lists all the modular cuts that are not empty
def listAllCuts(connectivity):
    return [ModularCut(basis, connectivity)
            for basis in [frozenset(s) for s in powerset(connectivity.subsets)]
            if basis != set()]

def elisionCuts(cutList):
    return [cut for cut in cutList if cut.isElision()]

def unitaryCuts(cutList):
    return [cut for cut in cutList if cut.isUnitary()]

def connectedCuts(cutList):
    return [cut for cut in cutList if cut.isConnected()]

