print("Enter numbers to find LCM of. Enter 0 to end input sequence.")
a=list()
while True:
    b=int(input())
    if b==0:
        break
    a.append(b)
print(a)
max = a[0]
for i in range(0,len(a)):
    if a[i]>max:
        max=a[i]
    else:
        continue
print(max)
lcm=max
f=False
while True:
    for i in range(0,len(a)):
        if lcm%a[i]!=0:
            f=False
            break
        else:
            f=True
    lcm+=1
    if f==False:
        continue
    else:
        break
print("LCM is",lcm-1)