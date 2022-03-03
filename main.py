import numpy as np
from copy import copy, deepcopy
# I was having some problems with recursion limits so I raised it slightly.
import sys
sys.setrecursionlimit(2000)

class Puzzlestate:
    """
    This Puzzlestate class will be used as a sort of node to represent a state that the
    puzzle is in. For each state that the puzzle is in, there can be multiple different
    states for each piece that could be moved next (children). Keeping track of these will allow
    for the ability to  find the best paths and to not repeat paths.
    """
    def __init__(self, puzzle, parent, goal):
        self.puzzle = puzzle
        self.goal = goal
        self.parent = parent
        self.visited = False
        self.solved = self.checksolved()
        self.children = []
        if self.parent is not None:
            self.g = self.parent.g + 1
        else:
            self.g = 1
        self.h1 = self.distance()
        self.h2 = self.misplaced()
        self.h3 = self.h1 + self.h2
        self.f = self.h1 + self.g
        self.f2 = self.h1 + self.h2 + self.g

    # method returns the puzzle states for each possible move
    def getmoves(self):
        newpuzzles = []
        for x in range(3):
            for y in range(3):
                if self.puzzle[x][y] == 0:
                    # there is only 1 position where there are 4 possible moves ( center )
                    if x == y and y == 1:
                        newpuzzles.append(self.swap(1, 1, 0, 1))
                        newpuzzles.append(self.swap(1, 1, 1, 0))
                        newpuzzles.append(self.swap(1, 1, 1, 2))
                        newpuzzles.append(self.swap(1, 1, 2, 1))
                    # below are all 8 other possible positions of the 0 empty tile
                    if x == 0:
                        if y == 0:
                            newpuzzles.append(self.swap(x, y, x + 1, y))
                            newpuzzles.append(self.swap(x, y, x, y + 1))
                        if y == 1:
                            newpuzzles.append(self.swap(x, y, x, y - 1))
                            newpuzzles.append(self.swap(x, y, x + 1, y))
                            newpuzzles.append(self.swap(x, y, x, y + 1))
                        if y == 2:
                            newpuzzles.append(self.swap(x, y, x + 1, y))
                            newpuzzles.append(self.swap(x, y, x, y - 1))
                    if x == 1:
                        if y == 0:
                            newpuzzles.append(self.swap(x, y, x + 1, y))
                            newpuzzles.append(self.swap(x, y, x, y + 1))
                            newpuzzles.append(self.swap(x, y, x - 1, y))
                        if y == 2:
                            newpuzzles.append(self.swap(x, y, x + 1, y))
                            newpuzzles.append(self.swap(x, y, x, y - 1))
                            newpuzzles.append(self.swap(x, y, x - 1, y))
                    if x == 2:
                        if y == 0:
                            newpuzzles.append(self.swap(x, y, x - 1, y))
                            newpuzzles.append(self.swap(x, y, x, y + 1))
                        if y == 1:
                            newpuzzles.append(self.swap(x, y, x, y - 1))
                            newpuzzles.append(self.swap(x, y, x - 1, y))
                            newpuzzles.append(self.swap(x, y, x, y + 1))
                        if y == 2:
                            newpuzzles.append(self.swap(x, y, x - 1, y))
                            newpuzzles.append(self.swap(x, y, x, y - 1))
        return newpuzzles

    # swap will return a 2d puzzle array with the new moves
    def swap(self, sourcex, sourcey, destinationx,destinationy):
        temp = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for x in range(3):
            for y in range(3):
                temp[x][y] = self.puzzle[x][y]
        tempvar = 0
        tempvar = temp[destinationx][destinationy]
        temp[destinationx][destinationy] = temp[sourcex][sourcey]
        temp[sourcex][sourcey] = tempvar
        return temp

    # count the number of misplaced tiles compared to the goalstate
    def misplaced(self):
        ct = 0
        tot = 0
        for row in self.goal:
            for tiles in row:
                if tiles is not self.puzzle[int(ct/3)][ct % 3]:
                    tot += 1
                ct += 1
        return tot

    # get the sum of manhattan distances of the tiles compared to their goalstate
    def distance(self):
        distancect = 0
        for z in range(9):
            for x in range(3):
                for y in range(3):
                    if self.puzzle[x][y] == self.goal[int(z/3)][z % 3]:
                        distancect += abs(x-int(z/3)) + abs(y-(z % 3))
        return distancect

    # chek if the puzzle is solved
    def checksolved(self):
        if self.puzzle == self.goal:
            return True
        else:
            return False


class aStarh1:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowesth1(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowesth1(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1

    def picklowesth1(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.f = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.f < min:
                min = child.f
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.f == min:
                return child
        node.f = 10000
        self.solution.pop()
        return node.parent

class aStarh2:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowesth2(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowesth2(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1


    def picklowesth2(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.h2 = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.h2 < min:
                min = child.h2
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.h2 == min:
                return child
        node.h2 = 10000
        self.solution.pop()
        return node.parent

class aStarh3:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowesth3(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowesth3(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1


    def picklowesth3(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.f2 = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.f2 < min:
                min = child.f2
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.f2 == min:
                return child
        node.f2 = 10000
        self.solution.pop()
        return node.parent

class best:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowestb1(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowestb1(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1


    def picklowestb1(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.h1 = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.h1 < min:
                min = child.h1
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.h1 == min:
                return child
        node.h1 = 10000
        self.solution.pop()
        return node.parent

class best2:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowestb2(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowestb2(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1


    def picklowestb2(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.h2 = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.h2 < min:
                min = child.h2
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.h2 == min:
                return child
        node.h2 = 10000
        self.solution.pop()
        return node.parent


class best3:
    def __init__(self, ps, goal, maxval):
        self.root = ps
        self.maximum = maxval
        self.counter = 1
        self.goal = goal
        self.solution = []
        self.used = []
        self.solved = False
        bestchild = self.picklowestb3(self.root)
        self.solution.append(bestchild)
        self.used.append(bestchild.puzzle)
        if bestchild.checksolved is True:
            self.solved = True
        while self.solved is not True and self.counter < self.maximum:
            bestchild = self.picklowestb3(bestchild)
            self.solution.append(bestchild)
            bestchild.visited = True
            self.used.append(bestchild.puzzle)
            self.counter += 1


    def picklowestb3(self, node):
        for moves in node.getmoves():
            if moves not in self.used:
                node.children.append(Puzzlestate(moves, node, self.goal))
        if len(node.children) == 0:
            node.h2 = 10000
            self.solution.pop()
            return node.parent
        min = 9999
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child

            if child.h3 < min:
                min = child.h3
        for child in node.children:
            if child.checksolved() == True:
                self.solved = True
                return child
            if child.h3 == min:
                return child
        node.h3 = 10000
        self.solution.pop()
        return node.parent


# puzzle is a 2d array where each index represents a tile. The array below represents an 8 tile puzzle looking like:
#                                           0   1   5
#                                           7   4   2
#                                           8   6   3
# 0 represents the blank tile.

# I decided to make each implementation of the heuristics and search algorithms its own class. This was pretty much
# just a brute force method of making the assignment actually work. This code could definitely be cleaned up

# Puz is the input puzzle array for the puzzlestate. Changing puz will change the outputs.
puz = [[4, 5, 2], [6, 0, 1], [8, 7, 3]]
goalstate = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
# maximum steps is being used to stop the search early if there is beginning to be too many steps.
maximumsteps = 10000
pz = Puzzlestate(puz, None, goalstate)

# A* SEARCHES
ast = aStarh1(pz, goalstate, maximumsteps)
ast2 = aStarh2(pz, goalstate, maximumsteps)
ast3 = aStarh3(pz, goalstate, maximumsteps)

# BEST FIRST SEARCHES
best1 = best(pz, goalstate, maximumsteps)
best2 = best2(pz, goalstate, maximumsteps)
best3 = best3(pz, goalstate, maximumsteps)


if ast.counter < ast.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 1: Steps = ", ast.counter)
    for sol in ast.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 1")

if ast2.counter < ast2.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 2: Steps = ", ast2.counter)
    for sol in ast2.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 2")

if ast3.counter < ast3.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 3: Steps = ", ast3.counter)
    for sol in ast3.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 3")

if best1.counter < best1.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 1 AND BEST FIRST: Steps = ", best1.counter)
    for sol in best1.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 1 with best first")

if best2.counter < best2.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 2 AND BEST FIRST: Steps = ", best2.counter)
    for sol in best2.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 2 with best first")

if best3.counter < best3.maximum:
    print(" SOLUTION STEPS USING HEURISTIC 3 AND BEST FIRST: Steps = ", best3.counter)
    for sol in best3.solution:
        print(sol.puzzle)
else:
    print(" Maximum number of steps reached for this puzzle using heuristic 3 with best first")


