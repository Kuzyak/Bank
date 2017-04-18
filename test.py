print ("Start")
p=3.37/12/100
n=180
k=10000000
a=k*(p+p/((1+p)**n-1))
#a=p*(((1+p)*n)/((1+p)*(n-1)))
print (a)
print (a*n)
print ("End")
