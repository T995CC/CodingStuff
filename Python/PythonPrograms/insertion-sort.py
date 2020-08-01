l=list(eval(input("Enter a list of numbers")))
for i in range(1,len(l)):
    x=l[i]
    for j in range(i-1,-1,-1):
        if l[j]>l[j+1]:
            l[j],l[j+1]=l[j+1],l[j]
        else:
            l[j+1]=x
            break
print(l)