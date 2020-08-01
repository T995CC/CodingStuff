a=int(input("Enter 1st number"))
b=int(input("Enter 2nd number"))

def hcf(m, n):
    if n==0:
        return m
    return hcf(n, m%n)

print("The HCF of ", a, " and ", b, " is ", hcf(a,b))