file1 = open("input.txt","r")
fuels = []
for fuel in file1:
    fuels.append(int(fuel))

def recursive_fuel(n):
    added_fuel = n // 3 - 2
    if added_fuel <= 0:
        return 0
    return added_fuel + recursive_fuel(added_fuel)

fuels = [recursive_fuel(i) for i in fuels]

print(sum(fuels))