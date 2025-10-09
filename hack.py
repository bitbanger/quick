import inspect, ctypes

def forceattr(tn, attr, val):
	try:
		return (getattr(tn,attr),setattr(tn,attr,val))[0]
	except TypeError as e:
		if 'immutable type' not in str(e):
			raise e

	(tp_flags:=ctypes.c_ulong.from_address(id(tn)+8*21)).value&=(~(1<<8))
	old = getattr(tn, attr)
	setattr(tn, attr, val)
	tp_flags.value|=(1<<8)
	return old

forceattr(dict, '__iter__', lambda s:dict.items(s).__iter__())

# TODO: only do this when I'm calling the code
# (and/or check the LoC of the caller to guess if they want a tuple?)
# (maybe change unpacking itself?)
for x in {1:2}:
	print(x)

quit()

# *They* don't want you to have this power:

try:
	dict.__iter__=lambda *a,**kw:(print('I lose'),dict.items(*a,**kw).__iter__())[1]
except Exception as e:
	assert(str(e)=="cannot set '__iter__' attribute of immutable type 'dict'")

# But *I* want to iterate over dictionaries without typing .items()

# So fuck it we're just going to edit the C structures
# for all dictionaries live in memory to make this change

# We can get the mem address for the dict structure in C
# using id()

# TPFLAGS are 21 bytes past the address of dict's id

# I counted them myself:
# https://github.com/python/cpython/blob/
	# e7e3d1d4a8dece01b1bbd0253684d5b46b2409d7/Include/cpython/object.h#L181

tp_flags = ctypes.c_ulong.from_address(id(dict) + 168)
assert(tp_flags.value == dict.__flags__) # see?

tp_flags.value &= -257	# wipe the immutable flag
												# (the cpython source code confirms it's bitmask 1<<8, aka 256)

# Do you know why you can't stop me from doing this anymore?
# It's because I'm just built different than you, Guido.
dict.__iter__=lambda *a,**kw:(print('I win'),dict.items(*a,**kw).__iter__())[1]

tp_flags.value |= 256

for x in {'abc': 123}:
	print(x)
