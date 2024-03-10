import copy

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
        return self.__parent == None

    def get_pos(self) -> tuple[int, int]:
        return copy.deepcopy(self.__pos)
    
    def set_pos(self, position: tuple[int, int]):
        self.__pos = position
    
    def get_obj_eaten(self) -> list[bool]:
        return copy.deepcopy(self.__obj_eaten)
    
    def set_obj_i_eaten(self, i: int):
        assert i >= 0 and i < self.__n - 1
        self.__obj_eaten[i] = True

    def set_parent(self, other: object):
        self.__parent = other
    
    def get_parent(self):
        return copy.deepcopy(self.__parent)

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
    
a = set([State((0, 0), [False, False, False]), State((1, 0), [False, True, False]), State((0, 0), [False, False, False])])
print(len(a))
