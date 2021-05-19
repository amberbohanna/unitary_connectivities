from modularcut import *
from functions import *
from main import *

groundset = frozenset([0, 1, 2])
bases = [frozenset([frozenset()]), frozenset([frozenset([0])]), frozenset([frozenset([0]), frozenset([1])]),
         frozenset([frozenset([0,1])])]
cuts = [ModularCut(bases[0], THREE), ModularCut(bases[1], THREE), ModularCut(bases[2], THREE),
        ModularCut(bases[3], THREE)]
functions = [
    # 0
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 1,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 0,
                  frozenset({0, 1})           : 1,
                  frozenset({0, 2})           : 1,
                  frozenset({0, 3})           : 1,
                  frozenset({1, 2})           : 1,
                  frozenset({1, 3})           : 1,
                  frozenset({2, 3})           : 1,
                  frozenset({0, 1, 2})        : 0,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 1,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3})),
    # 1
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 2,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 1,
                  frozenset({0, 1})           : 2,
                  frozenset({0, 2})           : 2,
                  frozenset({0, 3})           : 1,
                  frozenset({1, 2})           : 1,
                  frozenset({1, 3})           : 2,
                  frozenset({2, 3})           : 2,
                  frozenset({0, 1, 2})        : 1,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 2,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3})),
    # 2
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 1,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 1,
                  frozenset({0, 1})           : 2,
                  frozenset({0, 2})           : 1,
                  frozenset({0, 3})           : 1,
                  frozenset({1, 2})           : 1,
                  frozenset({1, 3})           : 1,
                  frozenset({2, 3})           : 2,
                  frozenset({0, 1, 2})        : 1,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 1,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3})),
    # 3
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 1,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 1,
                  frozenset({0, 1})           : 1,
                  frozenset({0, 2})           : 2,
                  frozenset({0, 3})           : 1,
                  frozenset({1, 2})           : 1,
                  frozenset({1, 3})           : 2,
                  frozenset({2, 3})           : 1,
                  frozenset({0, 1, 2})        : 1,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 1,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3})),
    # 4
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 1,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 1,
                  frozenset({0, 1})           : 1,
                  frozenset({0, 2})           : 1,
                  frozenset({0, 3})           : 2,
                  frozenset({1, 2})           : 2,
                  frozenset({1, 3})           : 1,
                  frozenset({2, 3})           : 1,
                  frozenset({0, 1, 2})        : 1,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 1,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3})),
    # 5
    Connectivity({frozenset()                 : 0,
                  frozenset({0})              : 1,
                  frozenset({1})              : 1,
                  frozenset({2})              : 1,
                  frozenset({3})              : 1,
                  frozenset({0, 1})           : 2,
                  frozenset({0, 2})           : 2,
                  frozenset({0, 3})           : 1,
                  frozenset({1, 2})           : 1,
                  frozenset({1, 3})           : 2,
                  frozenset({2, 3})           : 2,
                  frozenset({0, 1, 2})        : 1,
                  frozenset({0, 1, 3})        : 1,
                  frozenset({0, 2, 3})        : 1,
                  frozenset({1, 2, 3})        : 1,
                  frozenset({0, 1, 2, 3})     : 0},
                 frozenset({0, 1, 2, 3}))
]


def modularCutTest():
    # Tests that the correct cut is produced from a given basis
    constructionTest0()
    constructionTest1()
    constructionTest2()
    constructionTest3()

    # Tests that the correct function is produced in an extension
    extensionTest0()
    extensionTest1()
    extensionTest2()

    # Tests the isomorphism checking
    isoTest0()
    isoTest1()
    isoTest2()
    isoTest3()

    # Tests the isomorphism filtering
    isoFilterTest0()

def isoFilterTest0():
    for fun in filterIsomorphicConnectivities(functions):
        print(str(fun))

def isoTest0():
    assert functions[2].isomorphicTo(functions[3]), str(functions[2]) + " should be isomorphic to " \
        + str(functions[3])

def isoTest1():
    assert functions[3].isomorphicTo(functions[4]), str(functions[3]) + " should be isomorphic to " \
        + str(functions[4])

def isoTest2():
    assert not (functions[4].isomorphicTo(functions[5])), str(functions[4]) + " should not be isomorphic to " \
                + str(functions[5])

def isoTest3():
    assert not (functions[0].isomorphicTo(functions[3])), str(functions[0]) + " should not be isomorphic to " \
        + str(functions[3])

def extensionTest0():
    E0 = modularCutExtension(cuts[0], THREE)
    Expected = functions[0]

    assert E0 == Expected, str(E0) + " should be " + str(Expected)

def extensionTest1():
    E1 = modularCutExtension(cuts[1], THREE)
    Expected = functions[1]

    assert E1 == Expected, str(E1) + " should be " + str(Expected)

def extensionTest2():
    E2 = modularCutExtension(cuts[2], THREE)
    Expected = functions[2]

    assert E2 == Expected, str(E2) + " should be " + str(Expected)

def constructionTest0():
    Expected = frozenset([frozenset(s) for s in powerset(groundset)])
    
    # C0 should be the powerset of the ground set
    assert cuts[0].cut == Expected, str(cuts[0]) + " should be " + str(Expected)

def constructionTest1():
    Expected = frozenset([frozenset(sub) for sub in powerset(groundset) if 0 in sub])
    
    # C1 should be the subsets of the ground set containing 0
    assert cuts[1].cut == Expected, str(cuts[1]) + " should be " + str(Expected)

def constructionTest2():
    Expected = frozenset([frozenset([0]), frozenset([0, 1]), frozenset([0, 2]),
                          frozenset([0, 1, 2]), frozenset([1]), frozenset([1, 2])])

    # C2 should be the sets containing 0 or 1
    assert cuts[2].cut == Expected, str(cuts[2]) + " should be " + str(Expected)

def constructionTest3():
    Expected = frozenset([frozenset([0,1]), frozenset([0,1,2])])

    # C3 should be the set containing {0,1} and the ground
    assert cuts[3].cut == Expected, str(cuts[3]) + " should be " + str(Expected)

    
if __name__ == "__main__":
    modularCutTest()
