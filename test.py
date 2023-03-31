
from main import Term, Equation, isolate, Systems
from equaSystems import solveSystems


t = Term("-23")
print(repr(t.getLitCoef()))

a = Equation("1 + 4z = -2x -3y")
b = Equation("2y = -3x -z + 1")
c = Equation("0 = -4x - y - 2z +7")

d = Equation("2x + 3y = 5")
e = Equation("x + 4y = 7")

x = Systems(d, e)

s = Systems(a, b, c)
print("first print")
print(s)

print("remove column with var z")
s.remColumn("z1.0")
print(s)

s.multRow(1, 2)
print("rows")
print(s)


s.addToRow(rnum1=0, rnum2=1)
print("Added row2 to row1")
print(s)

solveSystems(x)
