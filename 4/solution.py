def strictly_increase(str_n):
    is_valid = True
    last_c = int(str_n[0])
    for j in range(1, len(str_n)):
        if int(str_n[j]) < last_c:
            is_valid = False
            break
        last_c = int(str_n[j])
    return is_valid

def dup_check(str_n):
    is_valid = False
    for dup in range(0, 10):
        str_grp = str(dup)*3
        str_dup = str(dup)*2
        if str_dup in str_n and str_grp not in str_n:
            is_valid = True
            break
    return is_valid

def check_valid(n):
    str_n = str(n)
    return strictly_increase(str_n) and dup_check(str_n)  

count = 0
for i in range(240298, 784957):
    if check_valid(i):
        count += 1

print(count)