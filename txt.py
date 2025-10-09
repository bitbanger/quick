import colors as c
import sys

from colors import colors

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

def spcspl(s):
	buf = []
	files = []
	for c in s:
		if len(buf)==0:
			buf.append(c)
			continue
		if c in (' ','\t','\n'):
			if buf[0] in (' ','\t','\n'):
				buf.append(c)
				continue
			else:
				files.append(''.join(buf))
				buf = [c]
		else:
			if buf[0] not in (' ','\t','\n'):
				buf.append(c)
				continue
			else:
				files.append(''.join(buf))
				buf = [c]

	return files


def main():
	s = sys.stdin.read()
	for e in spcspl(s):
		if e.endswith('.py'):
			e = rgb(e, *c.brightblue)
		print(e, end='')
	print('')


if __name__ == '__main__':
	main()
