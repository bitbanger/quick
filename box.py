import os
import re

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
def decolor(s):
	return ansi_escape.sub('', s)
# result = ansi_escape.sub('', sometext)

def box(content, pad=2):
	content = content.strip()

	ml = len(max(cspl:=content.split('\n'), key=lambda r: len(decolor(r))))
	for i, r in enumerate(cspl):
		while len(decolor(cspl[i])) < ml:
			cspl[i] += ' '
	content = '\n'.join(cspl)

	decolored = ansi_escape.sub('', content)
	import ll
	ll.rule()
	print(content)
	ll.rule()
	print(decolored)
	ll.rule()

	swid = os.get_terminal_size().columns
	
	chgt = len(spl:=decolored.split('\n'))
	cwid = len(max(spl, key=len))
	for _ in range(pad):
		for i, r in enumerate(spl):
			spl[i] = ' ' + r + ' '
		decolored = '\n'.join(spl)
		for i, r in enumerate(cspl:=content.split('\n')):
			cspl[i] = ' ' + r + ' '
		content = '\n'.join(cspl)

		content += '\n'+' '*(cwid+2*pad)
		content = ' '*(cwid+2*pad)+'\n' + content
		decolored += '\n'+' '*(cwid+2*pad)
		decolored = ' '*(cwid+2*pad)+'\n' + decolored

	chgt = len(spl:=decolored.split('\n'))
	cwid = len(max(spl, key=len))

	# ╭	╮	╰	╯│─
	buf = ''
	buf += '╭' + '─'*(cwid-2) + '╮' + '\n'

	cspl = content.split('\n')
	spl = decolored.split('\n')
	for i, l in enumerate(cspl):
		cspl[i] = '│' + l[1:-1]
		spl[i] += '│' + spl[i][1:-1]
		while len(spl[i]) < cwid:
			cspl[i] += ' '
			spl[i] += ' '
		cspl[i] += '│'
		spl[i] += '│'
	content = '\n'.join(cspl)
	decolored = '\n'.join(spl)
	buf += content
	buf += '\n' + '╰' + '─'*(cwid-2) + '╯' + '\n'

	return buf


	print(swid, cwid, chgt)
