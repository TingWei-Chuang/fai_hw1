# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Shang-Tse Chen (stchen@csie.ntu.edu.tw) on 03/03/2022

"""
This is the main entry point for HW1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

import maze as mz
from collections import deque
from copy import deepcopy
import heapq as pq
import numpy as np

class State:
    def __init__(self, position: tuple[int, int], objective_eaten: list[bool]) -> None:
        self.__pos = position
        self.__obj_eaten = objective_eaten
        self.__n = len(objective_eaten)
        self.__parent = None
        self.__cost = 0
        assert type(self.__pos) == tuple
        assert type(self.__obj_eaten) == list

    def is_root(self):
        return type(self.__parent) == type(None)

    def get_pos(self) -> tuple[int, int]:
        return deepcopy(self.__pos)
    
    def set_pos(self, position: tuple[int, int]):
        self.__pos = position
    
    def get_obj_eaten(self) -> list[bool]:
        return deepcopy(self.__obj_eaten)
    
    def set_obj_i_eaten(self, i: int):
        assert i >= 0 and i < self.__n
        self.__obj_eaten[i] = True

    def set_parent(self, other: object):
        self.__parent = other
    
    def get_parent(self):
        return deepcopy(self.__parent)

    def add_cost(self, cost: int):
        self.__cost += cost
    
    def get_cost(self):
        return self.__cost
    
    def all_dot_eaten(self):
        for i in range(self.__n):
            if not self.__obj_eaten[i]:
                return False
        return True
    
    def __eq__(self, other: object) -> bool:
        return self.__pos == other.__pos and self.__obj_eaten == other.__obj_eaten
    
    def __hash__(self) -> int:
        return hash((*self.__pos, *self.__obj_eaten))        

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def reach_goal(maze: mz.Maze, state: State):
    return maze.isObjective(*state.get_pos()) and state.all_dot_eaten()

def manhattan(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_astar(maze: mz.Maze, state: State):
    goal = maze.getObjectives()[0]
    current = state.get_pos()
    return manhattan(goal, current)

def heuristic_astar_corner(maze: mz.Maze, state: State):
    goal = maze.getObjectives()
    current = state.get_pos()
    obj_eaten = state.get_obj_eaten()
    candidate = []
    for i in range(len(goal)):
        if not obj_eaten[i]:
            candidate.append(manhattan(current, goal[i]))
    return min(candidate)

def bfs(maze: mz.Maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    objectives = maze.getObjectives()
    state = State(maze.getStart(), [False] * len(maze.getObjectives()))
    reached = set([state])
    fringe = deque([state])
    while len(fringe) > 0:
        prev_state = fringe.popleft()
        for pos in maze.getNeighbors(*prev_state.get_pos()):
            state = deepcopy(prev_state)
            state.set_pos(pos)
            if maze.isObjective(*pos):
                state.set_obj_i_eaten(objectives.index(pos))
            state.set_parent(prev_state)
            state.add_cost(1)
            if state in reached:
                continue
            # Goal Test
            if reach_goal(maze, state):
                # Return solution
                path = []
                s = state
                while not s.is_root():
                    path.append(s.get_pos())
                    s = s.get_parent()
                path.append(s.get_pos())
                path = path[::-1]
                return path
            reached.add(state)
            fringe.append(state)
    return []

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    state = State(maze.getStart(), [False] * len(maze.getObjectives()))
    reached = set([state])
    fringe = []
    idx = 0
    pq.heappush(fringe, (state.get_cost() + heuristic_astar(maze, state), idx, state))
    idx -= 1
    # debug
    visited = np.zeros(maze.getDimensions(), dtype=np.int8)
    visited[state.get_pos()[0], state.get_pos()[1]] = 1
    # debug
    while len(fringe) > 0:
        prev_state = pq.heappop(fringe)[2]
        for pos in maze.getNeighbors(*prev_state.get_pos()):
            state = deepcopy(prev_state)
            state.set_pos(pos)
            if maze.isObjective(*pos):
                state.set_obj_i_eaten(maze.getObjectives().index(pos))
            state.set_parent(prev_state)
            state.add_cost(1)
            if state in reached:
                continue
            # debug
            visited[state.get_pos()[0], state.get_pos()[1]] = 1
            # debug
            # Goal Test
            if reach_goal(maze, state):
                # Return solution
                path = []
                s = state
                while not s.is_root():
                    path.append(s.get_pos())
                    s = s.get_parent()
                path.append(s.get_pos())
                path = path[::-1]
                # debug
                for r in visited:
                    for c in r:
                        print('-' if not c else '.', end=' ')
                    print()
                visited[state.get_pos()[0], state.get_pos()[1]] = 1
                # debug
                return path
            reached.add(state)
            pq.heappush(fringe, (state.get_cost() + heuristic_astar(maze, state), idx, state))
            idx -= 1
    return []

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    state = State(maze.getStart(), [False] * len(maze.getObjectives()))
    reached = set([state])
    fringe = []
    idx = 0
    pq.heappush(fringe, (state.get_cost() + heuristic_astar_corner(maze, state), idx, state))
    idx -= 1
    while len(fringe) > 0:
        prev_state = pq.heappop(fringe)[2]
        for pos in maze.getNeighbors(*prev_state.get_pos()):
            state = deepcopy(prev_state)
            state.set_pos(pos)
            if maze.isObjective(*pos):
                state.set_obj_i_eaten(maze.getObjectives().index(pos))
            state.set_parent(prev_state)
            state.add_cost(1)
            if state in reached:
                continue
            # Goal Test
            if reach_goal(maze, state):
                # Return solution
                path = []
                s = state
                while not s.is_root():
                    path.append(s.get_pos())
                    s = s.get_parent()
                path.append(s.get_pos())
                path = path[::-1]
                return path
            reached.add(state)
            pq.heappush(fringe, (state.get_cost() + heuristic_astar_corner(maze, state), idx, state))
            idx -= 1
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
