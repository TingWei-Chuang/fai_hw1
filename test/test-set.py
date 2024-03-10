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

s = set()
s.add(obj1)
s.add(obj2)

print(len(s))