# from sympy import *

file1 = open("input.txt","r")
codes = file1.read().split(",")
codes = [int(i) for i in codes]
codes_copy = codes[:]

# codes[1] = symbols("x")
# codes[2] = symbols("y")

def run_program():
    for i in range(0, len(codes), 4):
        if codes[i] == 1 and i + 3 < len(codes):
            codes[codes[i+3]] = codes[codes[i+1]] + codes[codes[i+2]]
        elif codes[i] == 2 and i + 3 < len(codes):
            codes[codes[i+3]] = codes[codes[i+1]] * codes[codes[i+2]]
        elif codes[i] == 99:
            break

for n in range(0, 100):
    for v in range(0, 100):
        codes = codes_copy[:]
        codes[1] = n
        codes[2] = v
        run_program()
        if codes[0] == 19690720:
            print(100 * n + v)