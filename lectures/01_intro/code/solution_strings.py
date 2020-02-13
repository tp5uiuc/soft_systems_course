x = [chr(y) for y in range(ord('a'), ord('z')+1)]
print(x[::2])

# Pick and choose
y = x[::4]
z = [temp.upper() for temp in x[2::4]]
print(y)
print(z)


# List of double size allocate and then modify in place
a = x[::2]
a[::2] = y
a[1::2] = z
print(a)

y = x[3::4]
z = [temp.upper() for temp in x[1::4]]
q = x[1::2]
q[::2] = z
q[1::2] = y
print(q)
