import argparse
import quick.colors as c
import os
import pathlib
import re
import subprocess
import sys
import time

from contextlib import contextmanager

from quick.txt import rgb

try:
	os.get_terminal_size()
except:
	subprocess.run('ls')
	quit()

env=lambda k:os.environ.get(k)
home=lambda:env('HOME')or env('USERPROFILE')

def indent(s, n=1):
	return ('\t'*n) + '\n'.join(('\t'*n + l) for l in s.split('\n'))

def extrgb(s, *a, **kw):
	spl = s.split('.')
	if len(spl) == 1:
		return rgb(s, *a, **kw)

	ext = spl[-1]
	rest = '.'.join(spl[:-1])
	# return rest + rgb('.'+ext, *a, **kw)
	return rgb(rest, *a, **kw) + rgb('.' + ext, c.lightgray)

def ansi(s, num):
	# swap if num too long
	if isinstance(s, str) and isinstance(num, str) and len(s)<=3<len(num):
		s,num=num,s
	# swap if wrong types
	if isinstance(num, str) and isinstance(s, int):
		s,num=num,s

	# I read adding 20 to the code will undo only it
	# (except for bold/dim, which share dim's)
	end_code = num+20 if num != 1 else 22
	return f'\033[{num}m{s}\033[{end_code}m'

lansi = lambda c: lambda s: ansi(s, c)

bold = lansi(1)
dim = faint = lansi(2)
italic = italics = lansi(3)
underline = ul = lansi(4)
strikethrough = strikethru = strike = st = lansi(9)

class fi:
	__slots__='path','name','dot','dir','force_color'
	def __init__(self, path, force_color=None):
		self.path = path
		self.name = os.path.basename(path)
		self.dir = os.path.isdir(self.path)
		self.dot = self.name.startswith('.') or self.name.endswith('~') or self.name=='__pycache__'
		self.force_color = force_color


	def ansi(self):
		buf = ''
		s = self.__str__()
		while s.startswith('\033'):
			col = s.split('m')[0] + 'm'
			s = s[len(col):]
			buf += col
		return buf


	# TODO: stop being a coward & integrate with fmt
	def __str__(self):
		s = self.fmt()
		if self.dir:
			s = f'\033[1m{s}\033[0m'
		return s

	def fmt(self):
		# 🐭 It's a surprise tool that will help us later
		wrap = lambda x:x

		if self.force_color is not None:
			spl = self.force_color.split('/')

			mods = []
			for modcode in spl:
				if modcode in ('bold', 'bf', 'strong'):
					mods.append(bold)
				elif modcode in ('underline', 'ul', 'under'):
					mods.append(underline)
				elif modcode in ('italic', 'italics', 'it'):
					mods.append(italic)
				elif modcode in ('strikethrough', 'strikethru', 'strike', 'st'):
					mods.append(strike)
				elif (col:=c.colors.get(modcode)) is not None:
					mods.append(lambda x: rgb(x, col))

			fstr = self.name
			for mod in mods:
				fstr = mod(fstr)

			return fstr

		# At this point, they haven't requested
		# a specific color, so we can use a general
		# rule to color directories
		# TODO: move this to the lls file syntax/
		# base rules
		if self.dir:
			if self.dot:
				return bold(rgb(self.name, c.darkgreen))
			else:
				return bold(rgb(self.name, c.lightgreen))

		else:
			if self.dot:
				return extrgb(self.name, c.gray)
			else:
				ext = self.name.split('.')[-1].strip().lower()
				if ext in ('png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'):
					return extrgb(self.name, c.skyblue1)
				else:
					return extrgb(self.name)

	def __len__(self):
		from quick.box import decolor
		return len(decolor(self.name))

	def __lt__(self, other):
		return self.name<=other.name

@contextmanager
def clock():
	t0 = time.time()
	yield
	print(rgb(f'\t{time.time()-t0:.05f} secs', c.gray))


def rules(path):
	rs = []

	def _parse(l):
		spl = re.split('[ \t]+', l)
		col = spl[0]
		regex = re.compile(' '.join(spl[1:]))
		return regex, col

	# If a .lls file exists in the target dir, use it
	if os.path.exists(fn:=os.path.join(path, '.lls')):
		with open(fn, 'r') as f:
			txt = f.read()

		# lines starting with @ characters erase the previous newline
		for atch in re.findall('\n[ \t]*@', txt):
			txt = txt.replace(atch, '\t')

		for l in txt.splitlines():
			if not (l:=l.strip()):
				continue
			rs.append(_parse(l))

	# Always use the base rules last, so that they can be
	# superseded
	rs.extend([_parse(l) for l in BASE_LLS.splitlines() if l.strip()])

	# Build the fn->col function
	# TODO: smarter than taking the first match?
	def _lookup(fn):
		fn = os.path.basename(fn)
		for regex, col in rs:
			if regex.match(fn):
				return col
		return None

	return _lookup


def list_fs(path='.', ld=False, sort=True):
	path = norm_path(path)
	force_col_fn = rules(path)

	if ld:
		fs = [os.path.join(path, x) for x in os.listdir(path)]
	else:
		fs = [os.path.join(path, x.name) for x in os.scandir(path)]

	fs = [fi(f, force_color=force_col_fn(f)) for f in fs]

	if sort:
		dirs, dots, dotdirs, files = [],[],[],[]
		for f in fs:
			if f.dir and f.dot:
				dotdirs.append(f)
			elif f.dir:
				dirs.append(f)
			elif f.dot:
				dots.append(f)
			else:
				files.append(f)

		# Within each class of file, sort by color
	_gray = lambda f: isinstance(f.force_color, str) and 'gray' in f.force_color.lower()
	_sort_grays = lambda l: [e for e in l if not _gray(e)] + [e for e in l if _gray(e)]

	skey = lambda fil: (fil.ansi(), c.col_sort_key(fil.force_color))
	def skey(fil):
		name = fil.force_color or ''
		ansi = fil.ansi()

		# Everything but the color stays for the first key component
		cansi = c.name2ansi.get(name) or ''
		# print(name)
		# print(c.name2ansi.get(name))
		ansi = ansi.replace(cansi, '')

		# Then we'll split the ansi key up & sort it
		ansi_spl = tuple(sorted(x for x in ansi.split('\033') if x)) or ('',)
		# Then the color, by HSV
		hsv = c.hsv_sort_key(name)

		return ansi_spl + hsv

	_sort_col = lambda l: sorted(l, key=skey)
	# _sort_col = lambda l: sorted(l, key=lambda e: c.ansi2name[e.ansi()])
	# _sort_col = lambda l: (print(l), quit())[0]

	dirs = _sort_grays(_sort_col(sorted(dirs)))
	dotdirs = _sort_grays(_sort_col(sorted(dotdirs)))
	files = _sort_grays(_sort_col(sorted(files)))
	dots = _sort_grays(_sort_col(sorted(dots)))

	fs = dirs + dotdirs + files + dots

	fs = [f for f in fs if not _gray(f)] + [f for f in fs if _gray(f)]

	return fs


wwid = int(os.get_terminal_size().columns * 0.8)


class colinfo:
	__slots__ = 'valid', 'llen', 'mlen'
	def __init__(self, n):
		self.valid = True
		self.llen = 0
		self.mlen = [0]*n

def colcount(cfgs, fs):
	def strify(x):
		try:
			return x.name
		except AttributeError:
			return x

	mcw = 3 # min col width
	midx = int(wwid/mcw-1)
	lfs = len(fs)
	mcols = midx if midx<lfs else lfs

	for i, f in enumerate(fs):
		for j, cfg in enumerate(cfgs):
			if not cfg.valid:
				continue
			rs = int((lfs+j)/(j+1))
			if (rs*(j+1)-lfs) > rs:
				cfg.valid = False
				continue

			col = int(i/rs)
			from quick.box import decolor
			nw = len(decolor(strify(f)))

			if nw > (cml:=cfg.mlen[col]):
				cfg.llen += nw-cml
				cfg.mlen[col] = nw
			if cfg.llen+(2*j) > wwid:
				cfg.valid = False

	curs = mcols-1
	while curs>=0 and (not cfgs[curs].valid or not cfgs[curs].mlen[curs]):
		curs -= 1

	return curs+1

def fmt(fs):
	tcwid = os.get_terminal_size().columns
	global wwid
	mfsln = len(max(fs, key=len))
	if mfsln >= wwid:
		wwid = mfsln
	if mfsln >= tcwid:
		for f in fs:
			print(f)
		quit()

	st = ''

	st += ('\n')

	try:
		fs = [f for f in fs if not f.dot]
	except AttributeError:
		# We were passed something other than files
		pass

	lfs = len(fs)
	cfgs = [colinfo(i+1) for i in range(wwid)]

	nc = colcount(cfgs, fs)
	if nc == 0:
		# No files to list
		quit()

	nr = int((lfs+nc-1)/nc)

	for i in range(nr):
		for j in range(nc):
			fidx = i+j*nr
			if fidx>=lfs:
				continue
			st += str(fs[fidx])
			st += (' '*(cfgs[nc-1].mlen[j]-len(fs[fidx])))
			if j<nc-1:
				st += ('  ')
		st += ('\n')

	return st


def norm_path(path):
	if str(path).startswith('./') or str(path) == '.':
		path = os.path.join(os.path.relpath(os.getcwd()), str(path)[1:])
	if str(path).startswith('~'):
		path = str(path).replace('~', home())
	return pathlib.Path(path).absolute()


def lls(path='.', find=None, ld=False, sort=True):
	if isinstance(path, list):
		# We already did all the dirs in main, I guess
		fs = []
		for p in path:
			p = str(norm_path(p))
			pdir = os.path.dirname(p)
			p = os.path.relpath(p)
			force_col_fn = rules(pdir)
			fs.append(fi(p, force_color=force_col_fn(p)))
	else:
		path = norm_path(path)

		if os.path.isfile(path):
			fs = list_fs(path=os.path.dirname(path), ld=ld, sort=sort)
			fs = [f for f in fs if f.name==os.path.basename(path)]
		else:
			fs = list_fs(path=path, ld=ld, sort=sort)

	if len(fs) == 0:
		quit()

	fmted = fmt(fs)

	if find is not None:
		fmted = fmted.replace(find, rgb(find, c.red))

	return fmted


def lsf(pat, path='.', ld=False, sort=True):
	fstr = lls(path=path, ld=ld, sort=sort)
	fstr = fstr.replace(pat, rgb(pat, c.red))
	return fstr

BASE_LLS = ''
if os.path.exists(llsb:=os.path.join(os.environ.get('HOME'), '.lls_base')):
	with open(llsb, 'r') as f:
		BASE_LLS = f.read().strip()

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('paths', type=str, nargs='*', default=['.']) # TODO: path type (no internet rn)
	ap.add_argument('--find', '-f', type=str, default=None)
	args = ap.parse_args()

	paths = []
	for p in args.paths:
		if os.path.exists(p):
			paths.append(p)
		else:
			print(rgb("\ndoesn't exist: ", c.red) + p + '\n')

	if len(paths) == 1:
		print(lls(paths[0], find=args.find))
		quit()
	else:
		dirs = []
		fns = []
		for p in paths:
			if os.path.isdir(p):
				dirs.append(p)
			else:
				fns.append(p)

		for d in dirs:
			# print(f'[grey70]{d}[/grey70]:')
			print(rgb(d, 100, 100, 100) + ':', end='')
			print(indent(lls(args.paths, find=args.find), n=1))

	print(lls(fns, find=args.find))
	# for c in lls(args.path, find=args.find).encode():
		# print(hex(c))


if __name__ == '__main__':
	main()
