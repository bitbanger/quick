import argparse
import colors as c
import os
import pathlib
import re
import sys
import time

from txt import rgb
from contextlib import contextmanager

env=lambda k:os.environ.get(k)
home=lambda:env('HOME')or env('USERPROFILE')

def extrgb(s, *a, **kw):
	spl = s.split('.')
	if len(spl) == 1:
		return rgb(s, *a, **kw)

	ext = spl[-1]
	rest = '.'.join(spl[:-1])
	# return rest + rgb('.'+ext, *a, **kw)
	return rgb(rest, *a, **kw) + rgb('.' + ext, c.lightgray)

class fi:
	__slots__='path','name','dot','dir','force_color'
	def __init__(self, path, force_color=None):
		self.path = path
		self.name = os.path.basename(path)
		self.dir = os.path.isdir(self.path)
		self.dot = self.name.startswith('.') or self.name.endswith('~') or self.name=='__pycache__'
		self.force_color = force_color

	def __str__(self):
		if (self.force_color is not None) and ((fcol:=c.colors.get(self.force_color)) is not None):
			return rgb(self.name, fcol)

		if self.dir:
			if self.dot:
				return rgb(self.name, c.darkgreen)
			else:
				return rgb(self.name, c.lightgreen)

		else:
			if self.dot:
				return extrgb(self.name, c.gray)
			else:
				ext = self.name.split('.')[-1].strip().lower()
				if ext in ('png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'):
					return extrgb(self.name, c.skyblue)
				else:
					return extrgb(self.name)

	def __len__(self):
		from box import decolor
		return len(decolor(self.name))

	def __lt__(self, other):
		return self.name<=other.name

@contextmanager
def clock():
	t0 = time.time()
	yield
	print(rgb(f'\t{time.time()-t0:.05f} secs', c.gray))


def rules(path):
	if not os.path.exists(fn:=os.path.join(path, '.lls')):
		return lambda fn: None

	# Parse the rules from the file
	rs = []

	def _parse(l):
		spl = l.split(' ')
		col = spl[0]
		regex = re.compile(' '.join(spl[1:]))
		return regex, col

	with open(fn, 'r') as f:
		for l in f.readlines():
			if not (l:=l.strip()):
				continue
			rs.append(_parse(l))

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
		fs = sorted(dirs)+sorted(dotdirs)+sorted(files)+sorted(dots)

	return fs


wwid = int(os.get_terminal_size().columns * 0.8)


class colinfo:
	__slots__ = 'valid', 'llen', 'mlen'
	def __init__(self, n):
		self.valid = True
		self.llen = 0
		self.mlen = [0]*n

mcw = 3

def colcount(cfgs, fs):
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
			from box import decolor
			nw = len(decolor(f.name))

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

	fs = [f for f in fs if not f.dot]

	lfs = len(fs)
	cfgs = [colinfo(i+1) for i in range(wwid)]

	nc = colcount(cfgs, fs)
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
	if str(path).startswith('~'):
		path = str(path).replace('~', home())
	return pathlib.Path(path).absolute()


def lls(path='.', find=None, ld=False, sort=True):
	path = norm_path(path)

	if os.path.isfile(path):
		fs = list_fs(path=os.path.dirname(path), ld=ld, sort=sort)
		fs = [f for f in fs if f.name==os.path.basename(path)]
	else:
		fs = list_fs(path=path, ld=ld, sort=sort)

	fmted = fmt(fs)

	if find is not None:
		fmted = fmted.replace(find, rgb(find, c.red))

	return fmted


def lsf(pat, path='.', ld=False, sort=True):
	fstr = lls(path=path, ld=ld, sort=sort)
	fstr = fstr.replace(pat, rgb(pat, c.red))
	return fstr


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('path', type=str, nargs='?', default='.') # TODO: path type (no internet rn)
	ap.add_argument('--find', '-f', type=str, default=None)
	args = ap.parse_args()

	path = args.path
	

	print(lls(args.path, find=args.find))
	# for c in lls(args.path, find=args.find).encode():
		# print(hex(c))


if __name__ == '__main__':
	main()
