import os
import re
import sys

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
def decolor(s):
	return ansi_escape.sub('', s)

def fill_rect(content):
	decolored = decolor(content)

	content_split = content.split('\n')
	decolored_split = decolored.split('\n')

	max_len = len(max(decolored_split, key=len))

	for i in range(len(content_split)):
		if len(decolored_split[i]) < max_len:
			content_split[i] += ' '*(max_len-len(decolored_split[i]))

	content = '\n'.join(content_split)
	return content

	# ╭	╮	╰	╯│─
def _draw_box(
	content,
	ul='╭',
	ur='╮',
	ll='╰',
	lr='╯',
	h='─',
	v='│',
):
	while content.startswith('\n'):
		content = content[1:]
	while content.endswith('\n'):
		content = content[:-1]

	content = fill_rect(content)

	decolored = decolor(content)
	spl = content.split('\n')
	for i in range(len(spl)):
		spl[i] = v + spl[i] + v

	linelen = len(decolored.split('\n')[0])
	top = ul + h*linelen + ur
	bot = ll + h*linelen + lr

	spl = [top] + spl + [bot]
	return '\n'.join(spl)

def pad(content, c=' ', n=1):
	curs = content
	for _ in range(n):
		curs = _draw_box(curs, ul=c,ur=c,ll=c,lr=c,h=c,v=c)
	return curs

def box(content, padding=1):
	return _draw_box(pad(content, n=padding))


def dims(s):
	spl = s.split('\n')
	x = len(max(spl, key=len))
	y = len(spl)
	return x, y


from lls import tls
print(box(tls(sys.argv[1] if len(sys.argv)>1 else '~'), padding=0))
