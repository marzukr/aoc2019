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
        return self.output_buffer.pop(0)

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

robot = Computer(codes, [1])
painted = {(0,0): 1}
current_pos = (0,0)
orientation = (0,1)
while robot.run_program() == False:
    outputs = robot.output_all()
    painted[current_pos] = outputs[0]
    if outputs[1] == 0:
        orientation = (orientation[1] * -1, orientation[0])
    else:
        orientation = (orientation[1], orientation[0] * -1)
    current_pos = (current_pos[0] + orientation[0], current_pos[1] + orientation[1])
    if current_pos in painted:
        robot.receive_input([painted[current_pos]])
    else:
        robot.receive_input([0])

min_x = min(painted.keys())[0]
max_x = max(painted.keys())[0]
min_y = min(painted.keys(), key=lambda t: t[1])[1]
max_y = max(painted.keys(), key=lambda t: t[1])[1]
print(min_x, max_x, min_y, max_y)

width = max_x - min_x + 1
height = max_y - min_y + 1
print(width, height)

from PIL import Image
im = Image.new('1', (width, height))

for key, value in painted.items():
    real_coord = (key[0], key[1] * -1)
    im.putpixel(real_coord, value)
im.show()