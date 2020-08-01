a=int(input("Enter 1st number: "))
b=int(input("Enter 2nd number: "))

def hcf(m, n):
    if m==n:
        return m
    if m>=n:
        return hcf(m-n, n)
    return hcf(m, n-m)

print("The HCF of ", a, " and ", b, " is ", hcf(a,b))