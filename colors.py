import os
import sys

from colorsys import rgb_to_hsv

colors = {}
ansi2name = {}
name2ansi = {}

with open(os.path.join(os.path.dirname(__file__), 'data_colors.csv'), 'r') as f:
	this_module = sys.modules[__name__]
	for line in f.readlines():
		if not (line:=line.strip()):
			continue

		spl = line.split(',')
		cname = spl[0]
		col = tuple(int(x) for x in spl[1:])

		# Add the color to the dictionary
		colors[cname] = col

		from quick.txt import rgb
		ansi = rgb('', col).replace('\033[0m', '')
		ansi2name[ansi] = cname
		name2ansi[cname] = ansi

		# Add the color to the module
		setattr(this_module, cname, col)


def hsv_sort_key(cname):
	if cname not in colors:
		return -1,-1,-1
	r,g,b = colors.get(cname) or (-1,-1,-1)
	# return rgb_to_hsv(r,g,b)
	return rgb_to_hsv(r,g,b)


def main():
	from quick.txt import rgb
	for name, c in colors.items():
		print(rgb(name, *c))


if __name__ == '__main__':
	main()
