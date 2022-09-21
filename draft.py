class A:
    def __init__(self, a):
        self.value = a

a1 = A(1)
a2 = A(2)
a3 = A(3)
a4 = A(4)
a5 = A(5)
l = [a1, a2, a3, a4, a5]

total = sum([i.value for i in l])
print(total)