import math

asteroids = []
max_x = 0
max_y = 0
with open("input.txt","r") as file1:
    i = 0
    while True:
        line = file1.readline()
        if not line:
            break
        line = line.strip()
        max_x = len(line) - 1
        for j in range(0, len(line)):
            if line[j] == "#":
                asteroids.append((j, i))
        i += 1
    max_y = i - 1

# part 1
# max_detects = []
# for i in range(0, len(asteroids)):
#     can_see = {a:(True if a != asteroids[i] else False) for a in asteroids}
#     directions = 0
#     for key in can_see:
#         if can_see[key] == False:
#             continue

#         j = 1
#         to_test_i = (key[0] - asteroids[i][0], key[1] - asteroids[i][1])
#         divisor = max(math.gcd(to_test_i[0], to_test_i[1]), 1)
#         to_test_i = (to_test_i[0] // divisor, to_test_i[1] // divisor)

#         candidate = asteroids[i]
#         while candidate[0] <= max_x and candidate[1] <= max_y and candidate[0] >= 0 and candidate[1] >= 0:
#             candidate = (asteroids[i][0] + to_test_i[0] * j, asteroids[i][1] + to_test_i[1] * j)
#             if candidate in can_see:
#                 can_see[candidate] = False
#             j += 1
#         directions += 1
#     max_detects.append(directions)
# print(max(max_detects))
# print(max_detects.index(max(max_detects)))
# print(asteroids[262])

def laser_direction_gen(center):
    edge = (center[0], 0)
    direc = (edge[0] - )

laser_center = (29, 28)
laser_edge = (29, 0)
for i in range(0, len(asteroids)):
    can_see = {a:(True if a != asteroids[i] else False) for a in asteroids}
    directions = 0
    for key in can_see:
        if can_see[key] == False:
            continue

        j = 1
        to_test_i = (key[0] - asteroids[i][0], key[1] - asteroids[i][1])
        divisor = max(math.gcd(to_test_i[0], to_test_i[1]), 1)
        to_test_i = (to_test_i[0] // divisor, to_test_i[1] // divisor)

        candidate = asteroids[i]
        while candidate[0] <= max_x and candidate[1] <= max_y and candidate[0] >= 0 and candidate[1] >= 0:
            candidate = (asteroids[i][0] + to_test_i[0] * j, asteroids[i][1] + to_test_i[1] * j)
            if candidate in can_see:
                can_see[candidate] = False
            j += 1
        directions += 1
    max_detects.append(directions)