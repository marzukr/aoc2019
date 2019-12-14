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
        self.codes[0] = 2

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

import pyxel
import time

colors = {
    0: 0,
    1: 7,
    2: 12,
    3: 8,
    4: 3
}

class Arcade:
    def __init__(self):
        pyxel.init(44, 23)
        self.arcade = Computer(codes, [])
        self.last_ball_x = 0
        self.ball_x = 0
        self.paddle_x = 0
        self.joystick = []
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.joystick = [-1]
        elif pyxel.btn(pyxel.KEY_D):
            self.joystick = [1]
        elif pyxel.btn(pyxel.KEY_S):
            self.joystick = [0]
        else:
            self.joystick = []

    def draw(self):
        # pyxel.cls(0)
        self.arcade.run_program()
        tiles = self.arcade.output_all()

        for i in range(2, len(tiles), 3):
            x = tiles[i - 2]
            y = tiles[i - 1]
            tile_id = tiles[i]
            if x == -1 and y == 0:
                print("Score:", tile_id)
                continue
            if tile_id == 4:
                self.ball_x = x
            if tile_id == 3:
                self.paddle_x = x
            pyxel.pix(x, y, colors[tile_id])
        self.joystick = [0]
        if self.ball_x > self.last_ball_x and self.ball_x > self.paddle_x:
            self.joystick = [1]
        elif self.ball_x < self.last_ball_x and self.ball_x < self.paddle_x:
            self.joystick = [-1]
        self.last_ball_x = self.ball_x
        self.arcade.receive_input(self.joystick)
        # time.sleep(1/60)
        # input()

Arcade()
