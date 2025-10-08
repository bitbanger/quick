import sys
mymod = sys.modules[__name__]

with open('files/colors.csv', 'r') as f:
	for i, line in enumerate(f.readlines()):
		if i > 0:
			name, r, g, b = [x.strip() for x in line.strip().split(',')]
			setattr(mymod, name, (int(r),int(g),int(b)))

for v in ('name','r','g','b','i','f','line','v','mymod','x'):
	try:
		del globals()[v]
	except:
		pass

