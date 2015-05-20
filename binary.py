
print "{:3d} = {:06b} {:3d} = {:06b}".format( 8, 8, 7, 7)


xs = []
ys = []
for i in range(20):
    print "{:06b} {:3d}  -> {:06b} {:3d}".format(i,i, i & 7, i & 7)
    xs.append(i)
    ys.append( i & 7)

plot( xs, ys, 'bx-', markersize = 20)

savefig('binary.jpg')
