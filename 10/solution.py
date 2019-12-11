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
max_detects = []
asteroid_lines = []
laser_center = (29, 28)
# laser_center = (11,13)
for i in range(0, len(asteroids)):
    can_see = {a:(True if a != asteroids[i] else False) for a in asteroids}
    directions = 0
    this_asteroid_line = []
    for key in can_see:
        asteroids_in_line = []
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
                asteroids_in_line.append(candidate)
            j += 1
        directions += 1

        theta = math.acos((to_test_i[1] * -1) / math.sqrt(to_test_i[0] ** 2 + to_test_i[1] ** 2))
        if to_test_i[0] < 0:
            theta = 2*math.pi - theta
        this_asteroid_line.append((theta, asteroids_in_line))
    if asteroids[i] == laser_center:
        asteroid_lines = this_asteroid_line
    max_detects.append(directions)

asteroid_lines = sorted(asteroid_lines)
j = 0
for i in range(0, 200):
    print(asteroid_lines[j % len(asteroid_lines)][1].pop(0))
    j += 1