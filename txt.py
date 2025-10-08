import colors

def unhex(s):
	if s is None:
		return 255
	if type(s)==str:
		try:
			return int(s, 16)
		except ValueError:
			pass
	return s

def rgb(s, r=None, g=None, b=None):
	if type(r)==tuple and len(r)==3 and g is None and b is None:
		return rgb(s, *r)
	r,g,b = [unhex(x) for x in (r,g,b)]
	assert(all(type(x)==int for x in (r,g,b)))
	return f'\x1b[38;2;{r};{g};{b}m{s}\x1b[0m'

print(rgb('hi', colors.skyblue))
