from modularcut import *
from functions import *
from helper import *
import time

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

        print("Finding all cuts. ", end="")
        cuts = []
        number = 0
        for i in range(len(previousgen)):
            cuts.append(set(listCuts(previousgen[i])))
            number += len(cuts[i])
        print("Found " + str(number))

        number = 0
        for i in range(len(cuts)):
            cuts[i] = unitaryCuts(connectedCuts(cuts[i]))
            number += len(cuts[i])

        print("Of the cuts found, " + str(number) + " are elision, unitary, connected")
        
#        print("Removing isomorphic pairs of cuts. ", end="")
#        isopairs = len(cuts)
#        timestart = time.perf_counter()
#        cuts = filterIsomorphic(cuts)
# #       timestop = time.perf_counter()
# #       nonisopairs = len(cuts)
#        print("Removed " + str(isopairs - nonisopairs) + \
#              " in time " + str(timestop - timestart) + ".")
        
        print("Finding all extensions. ", end="")
        for i in range(len(previousgen)):
            for j in range(len(cuts[i])):
                nextgen.append(modularCutExtension(cuts[i][j], previousgen[i]))
        print("Found " + str(len(nextgen)))
        
        print("Finding non-isomorphic extensions. ", end="")
        nextgen = filterIsomorphicConnectivities(nextgen)
        print("Found " + str(len(nextgen)))

        for system in nextgen:
            print(str(system))
        
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

# print("Printing " + str(len(nextgen)) + \
        #       " Connectivity Functions:")
        # for system in nextgen:
        #     print(str(system))

        previousgen = nextgen
        nextgen = []
