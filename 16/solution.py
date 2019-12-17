nums = []
with open("input.txt","r") as file1:
    text = file1.readline().strip()
    for c in text:
        nums.append(int(c))
# nums = nums * 10000
new_list = nums[:]

def phase(l, n):
    for i in range(n, len(l)):
        # t = datetime.datetime.now()
        num_sum = 0
        multiple = i+1
        current = 0
        for j in range(i, len(l), multiple*2):
            to_add = sum(l[j:min(j+multiple, len(l))])
            if current % 2 == 0:
                num_sum += to_add
            else:
                num_sum -= to_add
            current += 1
        new_list[i] = abs(num_sum)%10
        # print((datetime.datetime.now() - t)*(len(l) - n)*100)

import datetime

t = datetime.datetime.now()
for i in range(0, 100):
    a = nums
    nums = new_list
    new_list = a
    # phase(nums, 5979187)
    print(i)
    phase(nums, 0)
print(new_list[0:8])
# print(new_list[5979187:(5979187+8)])
print(datetime.datetime.now() - t)