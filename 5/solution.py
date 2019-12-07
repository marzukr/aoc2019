file1 = open("input.txt","r")
codes = file1.read().split(",")
codes = [int(i) for i in codes]
codes_copy = codes[:]

input_val = 5

def interpret_instruction(instruction):
    number = instruction
    opcode = number % 100
    number //= 100
    param_modes = []
    while number > 0:
        param_modes.append(number % 10)
        number //= 10
    return (opcode, param_modes)

def get_value(value, params, param_n):
    if len(params) <= param_n or params[param_n] == 0:
        return codes[value]
    return value

def run_program():
    i = 0
    while True:
        instruction = interpret_instruction(codes[i])
        opcode = instruction[0]
        params = instruction[1]
        if opcode == 1 and i + 3 < len(codes):
            codes[codes[i+3]] = get_value(codes[i+1], params, 0) + get_value(codes[i+2], params, 1)
            i += 4
        elif opcode == 2 and i + 3 < len(codes):
            codes[codes[i+3]] = get_value(codes[i+1], params, 0) * get_value(codes[i+2], params, 1)
            i += 4
        elif opcode == 3 and i + 1 < len(codes):
            codes[codes[i+1]] = input_val
            i += 2
        elif opcode == 4 and i + 1 < len(codes):
            val = get_value(codes[i+1], params, 0)
            print(val)
            i += 2
        elif opcode == 5 and i + 2 < len(codes):
            if get_value(codes[i+1], params, 0) != 0:
                i = get_value(codes[i+2], params, 1)
            else:
                i += 3
        elif opcode == 6 and i + 2 < len(codes):
            if get_value(codes[i+1], params, 0) == 0:
                i = get_value(codes[i+2], params, 1)
            else:
                i += 3
        elif opcode == 7 and i + 3 < len(codes):
            if get_value(codes[i+1], params, 0) < get_value(codes[i+2], params, 1):
                codes[codes[i+3]] = 1
            else:
                codes[codes[i+3]] = 0
            i += 4
        elif opcode == 8 and i + 3 < len(codes):
            if get_value(codes[i+1], params, 0) == get_value(codes[i+2], params, 1):
                codes[codes[i+3]] = 1
            else:
                codes[codes[i+3]] = 0
            i += 4
        elif opcode == 99:
            break

run_program()