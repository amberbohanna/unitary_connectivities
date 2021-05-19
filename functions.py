from itertools import combinations, product, permutations, chain
from helper import powerset
import networkx as nx
import itertools as it
import matplotlib.pyplot as plt

# Class definitions for SetFunction, Connectivity, Polymatroid

# Submodular, Normal set function
class SetFunction:
    """A Submodular and Normalized function from Sets to Integers"""

    def __init__(self, mapping, groundset):
        """Initializer takes a dictionary (mapping) and a set (groundset)"""
        self.groundset = frozenset(groundset)
        self.subsets = [frozenset(s) for s in powerset(groundset)]
        self.mapping = mapping

    def __str__(self):
        """Prints the SetFunction"""
        #string = "Ground Set: \n\t" + str([s for s in self.groundset]) + "\n"
        #string = "Function: \n"
        graph = sorted([(k, v) for k, v in self.mapping.items()],
                       key = lambda x: x[1])

        curr = 0
        string = "0:\t"
        for (k, v) in graph:
            if v > curr:
                curr = v
                string += "\n" + str(v) + ":\t"
                string += str([s for s in k]) + " "
            else:
                string += str([s for s in k]) + " "
        string += "\n"
                
        return string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.groundset) == len(other.groundset):
                for sub in self.subsets:
                    if self.function(sub) != other.function(sub):
                        return False
                return True

    def function(self, A):
        """Apply the Set Function to the subset A"""
        if not (A <= self.groundset):
            raise Exception(str(A) + " isn't in " + str(self.groundset))
        return self.mapping[A]

    def isNormal(self):
        """True if the function is Normal"""
        for A in self.subsets:
            if self.function(A) < 0:
                return False
        return True
    
    def isSubmodular(self):
        """True if the function is Submodular"""
        triples = product(self.subsets, 3)
        E = groundset
        for (A, B, C) in triples:
            LHS = self.function(A) + self.function(B) + self.function(B)
            RHS = self.function(A&(E-B)&(E-C)) + \
                self.function((E-A)&B&(E-C)) + \
                self.function((E-A)&(E-B)&C)
            if LHS < RHS:
                return False
        return True

    def modular(self, p0, p1):
        """True if p0 and p1 are a modular pair"""
        return (self.function(p0) + self.function(p1) == 
                self.function(p0 & p1) + self.function(p0 | p1))
    
    def isValid(self):
        """True if the function is Normal and Submodular"""
        return self.isNormal() and self.isSubmodular

class Connectivity(SetFunction):
    """Connectivity system"""

    def __init__(self, mapping, groundset):
        """Takes a dictionary (mapping) and a set (groundset)"""
        super().__init__(mapping, groundset)
        self.graph = self.graph()

    @classmethod
    def from_poly(cls, polymatroid):
        """Constructor from a Polymatroid (polymatroid)"""
        conn = cls.__new__(cls)
        connMapping = {}
        for sub in polymatroid.subsets:
            connMapping[sub] = polymatroid.function(sub) - len(sub)
        super(cls, conn).__init__(connMapping, polymatroid.groundset)
        conn.graph = conn.graph()
        return conn

    def isSymmetric(self):
        """True if the value assigned to every set is the same as the value
           assigned to it's complement"""
        for A in self.subsets:
            if self.function(A) != self.function(self.groundset - A):
                return False
        return True

    def isValid(self):
        """True if the function is Normalized, Submodular and Symmetric"""
        return (super().isValid() and self.isSymmetric())

    def isUnitary(self):
        """True if all singletons are assigned the value 1"""
        for v in self.groundset:
            if self.function(set([v])) != 1:
                return False
        return True

    def isConnected(self):
        """True if no non-trivial subsets are assigned the value 0"""
        for s in self.subsets:
            if s != frozenset() and s != self.groundset:
                if self.function(s) == 0:
                    return False
        return True
   

    def stability(self, A, x):
        """Returns -1 if A is x-decreasing, 0 if A is x-neutral, 1 otherwise"""
        if not isinstance(x, frozenset):
            if isinstance(x, set):
                x = frozenset(x)
            if isinstance(x, int):
                x = frozenset([x])
            
        if self.function(A) > self.function(A | x): return -1
        if self.function(A) == self.function(A | x): return 0
        if self.function(A) < self.function(A | x): return 1

    def isomorphicTo(self, other):
        """Uses the permutations of the ground set to check isomorphism"""
        def relabel(perm, sub):
            """Relabels the subset according to the permutation given"""
            out = frozenset()
            for e in sub:
                out = out | set([perm[e]])
            return out
        
        ground = sorted(list(self.groundset))
        perms = list(permutations(ground))
        for perm in perms:
            iso = True
            for sub in self.subsets:
                if self.function(relabel(perm, sub)) != other.function(sub):
                    iso = False
                    break
            if iso:
                return True
        return False
        
    def graph(self):
        """Finds the isomorphism invariant digraph for this function"""
        def getSubset(s0, s1):
            if s0 <= s1:
                return (s0, s1)
            if s1 <= s0:
                return (s1, s0)

        G = nx.DiGraph()
        for s in self.subsets:
            for v in self.groundset - s:
                if self.stability(s, frozenset([v])) == -1:
                    G.add_edge(s, v)
                if self.stability(s, frozenset([v])) == 0:
                    G.add_edge(v, s)
                    G.add_edge(s, v)
                if self.stability(s, frozenset([v])) == 1:
                    G.add_edge(v, s)


        
        # Encode the connectivity structure of the sets
#        for s0, s1 in combinations(self.subsets, 2):
#            if len(s0 ^ s1) == 1:
#                e = s0 ^ s1
#                s0, s1 = getSubset(s0, s1)
#                if self.stability(s0, e) == -1: G.add_edge(s0, s1)
#                if self.stability(s0, e) == 1: G.add_edge(s1, s0)
        return G

# THE unique unitary connectivity function on three elements
THREE = Connectivity(
    {frozenset():0, frozenset({0}):1, frozenset({1}):1,
     frozenset({2}):1, frozenset({0,1}):1, frozenset({0,2}):1,
     frozenset({1,2}):1, frozenset({0,1,2}):0},
    {0,1,2}
)

# THE unique unitary connectivity function on two elements
TWO = Connectivity(
    {frozenset():0, frozenset([0]):1, frozenset([1]):1,
     frozenset([0,1]):0},
    {0,1}
)

# THE unique connectivity function on one element
ONE = Connectivity(
    {frozenset():0, frozenset([0]):0},
    {0}
)
    
class Polymatroid(SetFunction):
    """Polymatroid is a Set Function with the additional property Increasing"""
    def __init__(self, mapping, groundset):
        super().__init__(mapping, groundset)
        self.flats = set({self.closure(A) for A in self.subsets})
        self.nonflats = set(self.subsets) - self.flats
        self.graph = self.graph()

    @classmethod
    def from_conn(cls, connectivity):
        """Constructor from Connectivity (connectivity)"""
        poly = cls.__new__(cls)
        
        mapping = {}

        for A in connectivity.subsets:
            mapping[A] = sum([connectivity.function(frozenset([a])) for a in A]) + \
                connectivity.function(A)
            
        super(cls, poly).__init__(mapping, connectivity.groundset)

        poly.flats = set({poly.closure(A) for A in poly.subsets})
        poly.nonflats = set(poly.subsets) - poly.flats
        
        poly.graph = poly.graph()
        return poly

    def __str__(self):
        """Returns a string representation"""
        funcString = super().__str__()
        flatInfo = ""
        for flat in self.flats:
            flatInfo += "Flat: " + str(flat) + ", rank: " + \
                str(self.function(flat)) + "\n"
        return funcString + flatInfo
         
    def closure(self, A):
        """Finds the set containing A where any additional element increases the rank"""
        def closed(X, x):
            return self.function(X | frozenset([x])) == self.function(X)

        return frozenset({x for x in self.groundset if closed(A, x)})

    def isIncreasing(self):
        """True if for any pair A, B, with A a subset of B, function(A) < function(B)"""
        pairs = combinations(self.subsets, 2)
        for (A, B) in self.pairs:
            if A <= B and self.function(A) > self.function(B):
                return False
            if B <= A and self.function(B) > self.function(A):
                return False
        return True

    def isValid(self):
        """True if Normalized, Submodular and Increasing"""
        return super().isValid() and self.isIncreasing()

    def graph(self):
        """Returns the isomorphism invariant graph for this polymatroid"""
        G = nx.Graph()

        for e in self.groundset:
            G.add_node(e, color=-1)
            
        for f in self.flats:
            G.add_node(f, color=self.function(f))

        for e, f in product(self.groundset, self.flats):
            if e in f:
                G.add_edge(e, f)
                
        return G

def colors_match(n1_attrib,n2_attrib):
    """returns False if either does not have a color or if the colors do not match"""
    try:
        return n1_attrib['color']==n2_attrib['color']
    except KeyError:
        return False
    
# Filters out isomorphic polymatroids
def filterIsomorphicPolymatroids(polymatroids):
    reps = [polymatroids[0]]
    for polymatroid in polymatroids:
        newRep = True
        GN = polymatroid.graph
        for rep in reps:
            GR = rep.graph
            GM = nx.algorithms.isomorphism.GraphMatcher(GN, GR, node_match=colors_match)
            if GM.is_isomorphic():
                newRep = False
                print("found isomorphic")
                break
        if newRep:
            reps.append(polymatroid)            
    return reps
            
