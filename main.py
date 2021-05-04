from modularcut import *
from functions import *
from helper import *
import time

# Filters out isomorphic structures
def filterIsomorphic(structures):
    representatives = [structures[0]]
    for structure in structures:
        newRepresentative = True
        candidate = structure.graph
        for representative in representatives:
            rep = representative.graph
            if nx.is_isomorphic(candidate, rep):
                newRepresentative = False
        if newRepresentative:
            representatives.append(structure)            
    return representatives

# Filters out isomorphic structures
def filterIsomorphicConnectivities(structures):
    representatives = [structures[0]]
    for structure in structures:
        newRepresentative = True
        for representative in representatives:
            if structure.isomorphicTo(representative):
                newRepresentative = False
        if newRepresentative:
            representatives.append(structure)     
    return representatives


if __name__ == "__main__":
    previousgen = [TWO]
    size = len(previousgen[0].groundset)
    nextgen = []
    
    for i in range(5):
        print("Unitary functions with |E| = " + str(size + 1 + i) + ".")
        print("Finding all elision cuts. ", end="")

        timestart = time.perf_counter()
        cuts = []
        for system in previousgen:
            cuts += listCuts(system)
        timestop = time.perf_counter()
        print("Found " + str(len(cuts)) + " in time " + \
              str(timestop - timestart) + ".")

#        print("Removing isomorphic pairs of cuts. ", end="")
#        isopairs = len(cuts)
#        timestart = time.perf_counter()
#        cuts = filterIsomorphic(cuts)
# #       timestop = time.perf_counter()
# #       nonisopairs = len(cuts)
#        print("Removed " + str(isopairs - nonisopairs) + \
#              " in time " + str(timestop - timestart) + ".")
        
        print("Finding all extensions. ", end="")
        timestart = time.perf_counter()
        for system, cut in product(previousgen, cuts):
            nextgen.append(modularCutExtension(cut, system))
        timestop = time.perf_counter()
        print("Found " + str(len(nextgen)) + " in time " + \
              str(timestop - timestart))

        print("Filtering out isomorphic connectivities")
        nextgen = filterIsomorphicConnectivities(nextgen)
        
#        polys = [Polymatroid.from_conn(system) for system in nextgen]
#        nextpolys = filterIsomorphicPolymatroids(polys)
#        nextgen = [Connectivity.from_poly(poly) for poly in nextpolys]
        
#        print("Removing isomorphic pairs of functions. ", end="")
#        origlen = len(nextgen)
#        timestart = time.perf_counter()
#        nextgen = filterIsomorphic(nextgen)
#        timestop = time.perf_counter()
#        newlen = len(nextgen)
#        print("Removed " + str(origlen - newlen) + " in time " + \
#              str(timestop - timestart))

        print(str(len(nextgen)))
        # print("Printing " + str(len(nextgen)) + \
        #       " Connectivity Functions:")
        # for system in nextgen:
        #     print(str(system))

        previousgen = nextgen
        nextgen = []
