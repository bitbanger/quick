import colors as c
import os
import pathlib
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
	__slots__='path','name','dot','dir'
	def __init__(self, path):
		self.path = path
		self.name = os.path.basename(path)
		self.dir = os.path.isdir(self.path)
		self.dot = self.name.startswith('.') or self.name.endswith('~') or self.name=='__pycache__'

	def __str__(self):
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


def lls(path='.', ld=False, sort=True):
	if path.startswith('~'):
		path = path.replace('~', home())

	path = pathlib.Path(path).absolute()

	if ld:
		fs = [os.path.join(path, x) for x in os.listdir(path)]
	else:
		fs = [os.path.join(path, x.name) for x in os.scandir(path)]

	fs = [fi(f) for f in fs]

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
	__slots__='valid', 'llen', 'mlen'
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

def tab(fs):

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


def tls(*a, **kw):
	return tab(lls(*a, **kw))


def main():
	res = tab(lls(sys.argv[1] if len(sys.argv)>1 else '.'))
	print(res)
	quit()
	with clock():
		r = lls('.', ld=True)
	with clock():
		r2 = lls('.', ld=False)


if __name__ == '__main__':
	main()
