moons = []
moons_init = []
velocities = []
with open("input.txt","r") as file1:
    for line in file1:
        positions = line.split(",")
        positions = [int(i.replace("<", "").replace(">", "").replace("x", "").replace("y", "").replace("z", "").replace("=", "").strip()) for i in positions]
        positions = positions
        moons.append(positions)
        moons_init.append(positions[:])
        velocities.append([0,0,0])

def calculate_velocities():
    for i in range(0, len(moons)):
        for j in range(i + 1, len(moons)):
            for p in range(0, 3):
                if moons[i][p] < moons[j][p]:
                    velocities[i][p] += 1
                    velocities[j][p] += -1
                elif moons[i][p] > moons[j][p]:
                    velocities[i][p] += -1
                    velocities[j][p] += 1

def apply_velocity():
    for i in range(0, len(moons)):
        for p in range(0, 3):
            moons[i][p] += velocities[i][p]

def calc_energy():
    total = 0
    for j in range(0, len(moons)):
        potential = sum([abs(i) for i in moons[j]])
        kinetic = sum([abs(i) for i in velocities[j]])
        total += potential*kinetic
    return total

# for t in range(0, 1000):
#     calculate_velocities()
#     apply_velocity()
# print(calc_energy())

def check_axis(a):
    for i in range(0, len(moons)):
        if moons[i][a] != moons_init[i][a] or  velocities[i][a] != 0:
            return False
    return True

nums = []
for i in range(0, 3):
    t = 0
    while True:
        calculate_velocities()
        apply_velocity()
        t += 1
        if check_axis(i):
            break
    nums.append(t)
    moons = []
    for moon in moons_init:
        moons.append(moon[:])
    velocities = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

import math

lcm = nums[0]
for num in nums:
    lcm = (lcm * num) // math.gcd(lcm, num)
print(lcm)