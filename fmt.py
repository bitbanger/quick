import os


def dims():
	try:
		tcwid = os.get_terminal_size().columns
	except:
		tcwid = 100
	wwid = int(tcwid * 0.8)

	return (tcwid, wwid)


class colinfo:
	__slots__ = 'valid', 'llen', 'mlen'
	def __init__(self, n):
		self.valid = True
		self.llen = 0
		self.mlen = [0]*n


def colcount(cfgs, fs):
	tcwid, wwid = dims()

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


def fmt(fs, force_nc=None):
	tcwid, wwid = dims()
	
	mfsln = len(max(fs, key=len))
	if mfsln >= wwid:
		wwid = mfsln
	if mfsln >= tcwid:
		for f in fs:
			print(f)
		quit()

	st = ''

	st += ('\n')

	lfs = len(fs)
	cfgs = [colinfo(i+1) for i in range(wwid)]

	nc = colcount(cfgs, fs)
	if force_nc is not None:
		nc = force_nc
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
