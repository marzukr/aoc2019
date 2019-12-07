orbits = {}
with open("6/input.txt","r") as input_file:
    for line in input_file:
        objects = line.strip().split(")")
        if objects[0] in orbits:
            orbits[objects[0]].append(objects[1])
        else:
            orbits[objects[0]] = [objects[1]]

def count_orbits(object_orb, level):
    if object_orb not in orbits:
        return 0
    total = len(orbits[object_orb]) * level
    for orbiting in orbits[object_orb]:
        total += count_orbits(orbiting, level + 1)
    return total

# print(count_orbits("COM", 1))

def path_to_object(to_search, start):
    if start not in orbits:
        return None
    if to_search in orbits[start]:
        return [start]
    for orbiting in orbits[start]:
        result = path_to_object(to_search, orbiting)
        if result != None:
            return [start] + result

def distance(object1, object2):
    path1 = path_to_object(object1, "COM")
    path2 = path_to_object(object2, "COM")
    for i in range(0, min(len(path1), len(path2))):
        if path1[i] == path2[i]:
            continue
        return (len(path1) - i) + (len(path2) - i)

print(distance("SAN", "YOU"))

