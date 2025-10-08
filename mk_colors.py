import sys
with open('files/colors.csv', 'r') as f:
	for i, line in enumerate(f.readlines()):
		if i > 0:
			name, r, g, b = [x.strip() for x in line.strip().split(',')]
			name = name.replace(' ', '_').replace('-', '_')
			print(f'{name.lower()} = ({r}, {g}, {b})')
			print(f'{name.upper()} = ({r}, {g}, {b})')
