import numpy as np

with open("input.txt","r") as file:
    line = file.readline()
    layers = []
    for i in range(25*6, len(line), 25*6):
        layers.append(line[(i - 25*6):i])

    # part 1
    # min_zero = layers[0].count("0")
    # layer_i = 0
    # for i in range(1, len(layers)):
    #     count = layers[i].count("0")
    #     if count < min_zero:
    #         min_zero = count
    #         layer_i = i
    # print(layers[layer_i].count("1") * layers[layer_i].count("2"))

    # part 2
    final_image = []
    for i in range(0, len(layers[0])):
        for j in range(0, len(layers)):
            if layers[j][i] == "2":
                continue
            else:
                val = int(layers[j][i])
                if val == 1:
                    final_image.append("1")
                else:
                    final_image.append(" ")
                break
    final_image = np.array(final_image)
    final_image = np.resize(final_image, (6, 25))
    print(final_image)
    

