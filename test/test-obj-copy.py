class abc:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c
    def __eq__(self, __value: object) -> bool:
        return self.a == __value.a and self.b == __value.b
    def __hash__(self) -> int:
        return hash((self.a, self.b))

obj1 = abc(2, 34, 12)
obj2 = abc(2, 34, 3412)

print(id(obj1), id(obj2))

obj1 = obj2

print(id(obj1), id(obj2))

int1 = 43
int2 = 54

print(id(int1), id(int2))

int1 = int2

print(id(int1), id(int2))

int1 += 5

print(id(int1), id(int2))

obj1 = abc(2, 34, 12)
obj2 = obj1

print(id(obj1), id(obj2))

obj2.a = 439

print(id(obj1), id(obj2))

print(obj2.a)