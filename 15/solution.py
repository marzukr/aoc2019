file1 = open("input.txt","r")
codes = file1.read().split(",")
codes = [int(i) for i in codes]
codes_copy = codes[:]

class Computer:
    def __init__(self, codes, inputs):
        self.codes = codes[:]
        self.codes_copy = codes[:]
        self.inputs = inputs[:]
        self.output_buffer = []
        self.i = 0
        self.relative_base = 0
        self.memory = {}

    def reset(self, inputs):
        self.codes = self.codes_copy[:]
        self.inputs = inputs[:]
        self.output_buffer = []
        self.i = 0

    def get_input_val(self):
        if len(self.inputs) > 0:
            return self.inputs.pop(0)
        else:
            return None

    def receive_input(self, input_r):
        self.inputs += input_r

    def output_one(self):
        if len(self.output_buffer) > 0:
            return self.output_buffer.pop(0)
        return None

    def output_all(self):
        outputs = self.output_buffer[:]
        self.output_buffer = []
        return outputs

    @staticmethod
    def interpret_instruction(instruction):
        number = instruction
        opcode = number % 100
        number //= 100
        param_modes = []
        while number > 0:
            param_modes.append(number % 10)
            number //= 10
        return (opcode, param_modes)

    def __getitem__(self, position):
        if position >= len(self.codes):
            if position not in self.memory:
                self.memory[position] = 0
            return self.memory[position]
        return self.codes[position]

    def __setitem__(self, position, value):
        if position >= len(self.codes):
            self.memory[position] = value
            return
        self.codes[position] = value

    def get_value(self, value, params, param_n):
        if len(params) <= param_n or params[param_n] == 0:
            return self[value]
        elif params[param_n] == 2:
            return self[self.relative_base + value]
        return value

    def set_value(self, value, position, params, param_n):
        if len(params) <= param_n or params[param_n] == 0:
            self[position] = value
        elif params[param_n] == 2:
            self[self.relative_base + position] = value

    def run_program(self):
        while True:
            instruction = Computer.interpret_instruction(self[self.i])
            opcode = instruction[0]
            params = instruction[1]
            if opcode == 1:
                val = self.get_value(self[self.i+1], params, 0) + self.get_value(self[self.i+2], params, 1)
                self.set_value(val, self[self.i+3], params, 2)
                self.i += 4
            elif opcode == 2:
                val = self.get_value(self[self.i+1], params, 0) * self.get_value(self[self.i+2], params, 1)
                self.set_value(val, self[self.i+3], params, 2)
                self.i += 4
            elif opcode == 3:
                val = self.get_input_val()
                if val != None:
                    self.set_value(val, self[self.i+1], params, 0)
                else:
                    return False
                self.i += 2
            elif opcode == 4:
                val = self.get_value(self[self.i+1], params, 0)
                self.output_buffer.append(val)
                self.i += 2
            elif opcode == 5:
                if self.get_value(self[self.i+1], params, 0) != 0:
                    self.i = self.get_value(self[self.i+2], params, 1)
                else:
                    self.i += 3
            elif opcode == 6:
                if self.get_value(self[self.i+1], params, 0) == 0:
                    self.i = self.get_value(self[self.i+2], params, 1)
                else:
                    self.i += 3
            elif opcode == 7:
                if self.get_value(self[self.i+1], params, 0) < self.get_value(self[self.i+2], params, 1):
                    self.set_value(1, self[self.i+3], params, 2)
                else:
                    self.set_value(0, self[self.i+3], params, 2)
                self.i += 4
            elif opcode == 8:
                if self.get_value(self[self.i+1], params, 0) == self.get_value(self[self.i+2], params, 1):
                    self.set_value(1, self[self.i+3], params, 2)
                else:
                    self.set_value(0, self[self.i+3], params, 2)
                self.i += 4
            elif opcode == 9:
                self.relative_base += self.get_value(self[self.i+1], params, 0)
                self.i += 2
            elif opcode == 99:
                return True

robot = Computer(codes, [])
output = 1
direction = 1
items = {}
pos = (0, 0)
oxygen = (0,0)
compass = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}
right = {
    1: 4,
    2: 3,
    3: 1,
    4: 2
}
inverse = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}
nodes = {}

def add_node(p1, p2):
    if p1 in nodes and p2 not in nodes[p1]:
        nodes[p1] += [p2]
    elif p1 not in nodes:
        nodes[p1] = [p2]
    if p2 in nodes and p1 not in nodes[p2]:
        nodes[p2] += [p1]
    elif p2 not in nodes:
        nodes[p2] = [p1]

start = True
while pos != (0,0) or start:
    robot.receive_input([right[direction]])
    robot.run_program()
    output = robot.output_one()
    if output == 0:
        wall = (pos[0] + compass[right[direction]][0], pos[1] + compass[right[direction]][1])
        items[wall] = output
        robot.receive_input([direction])
        robot.run_program()
        output = robot.output_one()
        if output == 0:
            direction = right[right[right[direction]]]
        else:
            blank = (pos[0] + compass[direction][0], pos[1] + compass[direction][1])
            add_node(pos, blank)
            pos = blank
            items[blank] = output
            start = False
    else:
        direction = right[direction]
        blank = (pos[0] + compass[direction][0], pos[1] + compass[direction][1])
        add_node(pos, blank)
        pos = blank
        items[blank] = output
        start = False
    if output == 2:
        oxygen = pos
items[(0,0)] = -1

min_x = min(items.keys())[0]
max_x = max(items.keys())[0]
width = max_x - min_x + 1
min_y = min(items.keys(), key=lambda n: n[1])[1]
max_y = max(items.keys(), key=lambda n: n[1])[1]
height = max_y - min_y + 1

from PIL import Image
im = Image.new('RGB', (width, height))
for key, value in items.items():
    real_coord = (key[0] + abs(min_x), max_y - key[1])
    color = (0,0,0)
    if value == 0:
        color = (255,255,255)
    elif value == 1:
        color = (0,0,255)
    elif value == 2:
        color = (0,255,0)
    elif value == -1:
        color = (255,0,0)
    im.putpixel(real_coord, color)
im.show()

distances = {key:1e6 for key in nodes}
distances[(0,0)] = 0


def dijkstra(start, end):
    for node in nodes[start]:
        if node not in distances:
            continue
        if distances[start] + 1 < distances[node]:
            distances[node] = distances[start] + 1
    if start == end:
        return distances[end]
    distances.pop(start, None)
    min_node = min(distances, key=distances.get)
    return dijkstra(min_node, end)

# print(dijkstra((0,0), oxygen))

oxygens = {key:False for key in nodes}
oxygens[(0,0)] = True
def oxygen_f(start, depth):
    depths = []
    for neighbor in nodes[start]:
        if oxygens[neighbor] == False:
            oxygens[neighbor] = True
            depths.append(oxygen_f(neighbor, depth + 1))
    if len(depths) == 0:
        return depth
    return max(depths)
print(oxygen_f(oxygen, 0))
    
        