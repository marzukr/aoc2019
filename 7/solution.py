file1 = open("7/input.txt","r")
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

    def interpret_instruction(instruction):
        number = instruction
        opcode = number % 100
        number //= 100
        param_modes = []
        while number > 0:
            param_modes.append(number % 10)
            number //= 10
        return (opcode, param_modes)

    def get_value(self, value, params, param_n):
        if len(params) <= param_n or params[param_n] == 0:
            return self.codes[value]
        return value

    def run_program(self):
        while True:
            instruction = Computer.interpret_instruction(self.codes[self.i])
            opcode = instruction[0]
            params = instruction[1]
            if opcode == 1 and self.i + 3 < len(self.codes):
                self.codes[self.codes[self.i+3]] = self.get_value(self.codes[self.i+1], params, 0) + self.get_value(self.codes[self.i+2], params, 1)
                self.i += 4
            elif opcode == 2 and self.i + 3 < len(self.codes):
                self.codes[self.codes[self.i+3]] = self.get_value(self.codes[self.i+1], params, 0) * self.get_value(self.codes[self.i+2], params, 1)
                self.i += 4
            elif opcode == 3 and self.i + 1 < len(self.codes):
                val = self.get_input_val()
                if val != None:
                    self.codes[self.codes[self.i+1]] = val
                else:
                    return False
                self.i += 2
            elif opcode == 4 and self.i + 1 < len(self.codes):
                val = self.get_value(self.codes[self.i+1], params, 0)
                self.output_buffer.append(val)
                self.i += 2
            elif opcode == 5 and self.i + 2 < len(self.codes):
                if self.get_value(self.codes[self.i+1], params, 0) != 0:
                    self.i = self.get_value(self.codes[self.i+2], params, 1)
                else:
                    self.i += 3
            elif opcode == 6 and self.i + 2 < len(self.codes):
                if self.get_value(self.codes[self.i+1], params, 0) == 0:
                    self.i = self.get_value(self.codes[self.i+2], params, 1)
                else:
                    self.i += 3
            elif opcode == 7 and self.i + 3 < len(self.codes):
                if self.get_value(self.codes[self.i+1], params, 0) < self.get_value(self.codes[self.i+2], params, 1):
                    self.codes[self.codes[self.i+3]] = 1
                else:
                    self.codes[self.codes[self.i+3]] = 0
                self.i += 4
            elif opcode == 8 and self.i + 3 < len(self.codes):
                if self.get_value(self.codes[self.i+1], params, 0) == self.get_value(self.codes[self.i+2], params, 1):
                    self.codes[self.codes[self.i+3]] = 1
                else:
                    self.codes[self.codes[self.i+3]] = 0
                self.i += 4
            elif opcode == 99:
                return True

# part 1
# from itertools import permutations
# perm = permutations(list(range(0, 5)))

# max_signal = 0
# for setting in list(perm):
#     output = 0
#     for thruster in setting:
#         computer = Computer(codes, [thruster, output])
#         computer.run_program()
#         output = computer.output()
#     if output > max_signal:
#         max_signal = output

# part 2
from itertools import permutations
perm = permutations(list(range(5, 10)))

max_signal = 0
for setting in list(perm):
    a = Computer(codes, [setting[0], 0])
    b = Computer(codes, [setting[1]])
    c = Computer(codes, [setting[2]])
    d = Computer(codes, [setting[3]])
    e = Computer(codes, [setting[4]])
    computers = [a,b,c,d,e]
    status_list = [False] * 5

    i = 0
    e_output = 0
    while False in status_list:
        status = computers[i%5].run_program()
        status_list[i%5] = status
        outputs = computers[i%5].output_all()
        if i % 5 == 4:
            e_output = outputs
        computers[(i+1)%5].receive_input(outputs)
        i += 1

    if e_output[0] > max_signal:
        max_signal = e_output[0]

print(max_signal)