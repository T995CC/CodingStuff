print("Enter numbers to find HCF of. Enter 0 to end input sequence.")
a = list()
while True:
    b = int(input())
    if b == 0:
        break
    a.append(b)
print(a)
min = a[0]
for i in range(0, len(a)):
    if a[i] < min:
        min = a[i]
    else:
        continue
print(min)
hcf = min
f = False
while True:
    for i in range(len(a)-1, -1, -1):
        if a[i] % hcf != 0:
            f = False
            break
        else:
            f = True
    hcf -= 1
    if f == False:
        continue
    else:
        break
print("HCF is", hcf+1)
