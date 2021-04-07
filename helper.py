# Helper functions and definitions that don't need to be anywhere else

from itertools import chain, combinations
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# Filters out isomorphic structures
def filterIsomorphic(structures):
    representatives = [structures[0]]
    for structure in structures:
        newRepresentative = True
        candidate = structure.graph
        for representative in representatives:
            rep = representative.graph
            DiGM = nx.algorithms.isomorphism.DiGraphMatcher(candidate, rep)
            if DiGM.is_isomorphic():
                newRepresentative = False
        if newRep:
            representatives.append(structure)            
    return representatives


