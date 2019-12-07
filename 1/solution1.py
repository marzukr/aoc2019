file1 = open("input.txt","r")
fuels = []
for fuel in file1:
    fuels.append(int(fuel))
fuels = [i // 3 - 2 for i in fuels]
print(sum(fuels))