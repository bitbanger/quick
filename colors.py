import inspect
import re




import ctypes


# So fuck it we're just going to edit the C structures
# for all dictionaries live in memory to make this change

# Let's do some magic

# TPFLAGS are 21 bytes past the address of dict's id
# I counted them myself:
# https://github.com/python/cpython/blob/
	# e7e3d1d4a8dece01b1bbd0253684d5b46b2409d7/Include/cpython/object.h#L181

# We can get the mem address for the dict structure in C
# using id()
tp_flags = ctypes.c_ulong.from_address(id(dict) + 168)
assert(tp_flags.value == dict.__flags__) # if this doesn't work we should NOT go farther

# let's go farther :)
tp_flags.value &= -257	# wipe the immutable flag
												# (the cpython source code confirms it's bitmask 1<<8, aka 256)


# Do you know why you can't stop me from doing this anymore?
# It's because I'm just built different than you, Guido.
old=dict.items;dict.__iter__=lambda *a,**kw:(print('I win'),old(*a,**kw).__iter__())[1]

tp_flags.value |= 256

for x in {'abc': 123}:
	print(x)











quit()
def getline(fn, n):
	with open(fn, 'r') as f:
		for i, l in enumerate(f.readlines()):
			if i==n-1:
				return l

__builtins__.dict.__iter__ = lambda *a,**kw: print('hi')
try:
	old_dict = __builtins__['dict']
except:
	old_dict = __builtins__.dict
class ldict(dict):
	def __iter__(self):
		return self.items().__iter__()

'''
	def __next__(self):
		ff = inspect.currentframe().f_back
		print(ff.f_code.co_filename)
		if 'python3' in ff.f_code.co_filename:
			return old_dict.__next__(self)
		caller_line = getline(ff.f_code.co_filename, ff.f_lineno)
		print(ff.f_code.co_filename)
		
		try:
			__builtins__['dict'] = old_dict
		except:
			__builtins__.dict = old_dict
		ms = re.findall('for (.*) in .*', caller_line)
		if len(ms)==1:
			unpack = [x.strip() for x in ms[0].split(',')]
			if len(unpack)==2:
				return 
		print(ms)
		quit()
		try:
			__builtins__['dict'] = self.__class__
		except:
			__builtins__.dict = self.__class__
		return None
'''
try:
	__builtins__.dict = ldict
except AttributeError:
	__builtins__['dict'] = ldict

aliceblue = (240, 248, 255)
aqua = (0, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
blueviolet = (138, 43, 226)
brown = (165, 42, 42)
chartreuse = (127, 255, 0)
chocolate = (210, 105, 30)
cornflowerblue = (100, 149, 237)
crimson = (220, 20, 60)
cyan = (0, 255, 255)
darkblue = (0, 0, 139)
darkgray = (169, 169, 169)
darkgreen = (0, 100, 0)
darkorange = (255, 140, 0)
darkred = (139, 0, 0)
darkviolet = (148, 0, 211)
deeppink = (255, 20, 147)
deepskyblue = (0, 191, 255)
dimgray = (105, 105, 105)
dodgerblue = (30, 144, 255)
firebrick = (178, 34, 34)
forestgreen = (34, 139, 34)
fuchsia = (255, 0, 255)
gainsboro = (220, 220, 220)
gold = (255, 215, 0)
goldenrod = (218, 165, 32)
gray = (128, 128, 128)
green = (0, 128, 0)
hotpink = (255, 105, 180)
indianred = (205, 92, 92)
indigo = (75, 0, 130)
khaki = (240, 230, 140)
lavender = (230, 230, 250)
lawngreen = (124, 252, 0)
lightblue = (173, 216, 230)
lightcoral = (240, 128, 128)
lightgray = (211, 211, 211)
lightgreen = (144, 238, 144)
lightpink = (255, 182, 193)
lightsalmon = (255, 160, 122)
lightslategray = (119, 136, 153)
lightsteelblue = (176, 196, 222)
lightyellow = (255, 255, 224)
lime = (0, 255, 0)
limegreen = (50, 205, 50)
magenta = (255, 0, 255)
maroon = (128, 0, 0)
material_amber = (255, 193, 7)
material_blue = (33, 150, 243)
material_cyan = (0, 188, 212)
material_deep_orange = (255, 87, 34)
material_deep_purple = (103, 58, 183)
material_green = (76, 175, 80)
material_indigo = (63, 81, 181)
material_light_blue = (3, 169, 244)
material_light_green = (139, 195, 74)
material_lime = (205, 220, 57)
material_orange = (255, 152, 0)
material_pink = (233, 30, 99)
material_purple = (156, 39, 176)
material_red = (244, 67, 54)
material_teal = (0, 150, 136)
material_yellow = (255, 235, 59)
mediumorchid = (186, 85, 211)
mediumseagreen = (60, 179, 113)
midnightblue = (25, 25, 112)
navy = (0, 0, 128)
olive = (128, 128, 0)
orange = (255, 165, 0)
orangered = (255, 69, 0)
peru = (205, 133, 63)
pink = (255, 192, 203)
plum = (221, 160, 221)
powderblue = (176, 224, 230)
purple = (128, 0, 128)
red = (255, 0, 0)
royalblue = (65, 105, 225)
salmon = (250, 128, 114)
sandybrown = (244, 164, 96)
sienna = (160, 82, 45)
silver = (192, 192, 192)
skyblue = (135, 206, 235)
slategray = (112, 128, 144)
springgreen = (0, 255, 127)
steelblue = (70, 130, 180)
tan = (210, 180, 140)
teal = (0, 128, 128)
tomato = (255, 99, 71)
violet = (238, 130, 238)
webgray = (102, 102, 102)
websafe_blue = (0, 0, 204)
websafe_green = (0, 204, 0)
websafe_red = (204, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
colors = dict({
	'aliceblue': aliceblue,
	'aqua': aqua,
	'black': black,
	'blue': blue,
	'blueviolet': blueviolet,
	'brown': brown,
	'chartreuse': chartreuse,
	'chocolate': chocolate,
	'cornflowerblue': cornflowerblue,
	'crimson': crimson,
	'cyan': cyan,
	'darkblue': darkblue,
	'darkgray': darkgray,
	'darkgreen': darkgreen,
	'darkorange': darkorange,
	'darkred': darkred,
	'darkviolet': darkviolet,
	'deeppink': deeppink,
	'deepskyblue': deepskyblue,
	'dimgray': dimgray,
	'dodgerblue': dodgerblue,
	'firebrick': firebrick,
	'forestgreen': forestgreen,
	'fuchsia': fuchsia,
	'gainsboro': gainsboro,
	'gold': gold,
	'goldenrod': goldenrod,
	'gray': gray,
	'green': green,
	'hotpink': hotpink,
	'indianred': indianred,
	'indigo': indigo,
	'khaki': khaki,
	'lavender': lavender,
	'lawngreen': lawngreen,
	'lightblue': lightblue,
	'lightcoral': lightcoral,
	'lightgray': lightgray,
	'lightgreen': lightgreen,
	'lightpink': lightpink,
	'lightsalmon': lightsalmon,
	'lightslategray': lightslategray,
	'lightsteelblue': lightsteelblue,
	'lightyellow': lightyellow,
	'lime': lime,
	'limegreen': limegreen,
	'magenta': magenta,
	'maroon': maroon,
	'material_amber': material_amber,
	'material_blue': material_blue,
	'material_cyan': material_cyan,
	'material_deep_orange': material_deep_orange,
	'material_deep_purple': material_deep_purple,
	'material_green': material_green,
	'material_indigo': material_indigo,
	'material_light_blue': material_light_blue,
	'material_light_green': material_light_green,
	'material_lime': material_lime,
	'material_orange': material_orange,
	'material_pink': material_pink,
	'material_purple': material_purple,
	'material_red': material_red,
	'material_teal': material_teal,
	'material_yellow': material_yellow,
	'mediumorchid': mediumorchid,
	'mediumseagreen': mediumseagreen,
	'midnightblue': midnightblue,
	'navy': navy,
	'olive': olive,
	'orange': orange,
	'orangered': orangered,
	'peru': peru,
	'pink': pink,
	'plum': plum,
	'powderblue': powderblue,
	'purple': purple,
	'red': red,
	'royalblue': royalblue,
	'salmon': salmon,
	'sandybrown': sandybrown,
	'sienna': sienna,
	'silver': silver,
	'skyblue': skyblue,
	'slategray': slategray,
	'springgreen': springgreen,
	'steelblue': steelblue,
	'tan': tan,
	'teal': teal,
	'tomato': tomato,
	'violet': violet,
	'webgray': webgray,
	'websafe_blue': websafe_blue,
	'websafe_green': websafe_green,
	'websafe_red': websafe_red,
	'white': white,
	'yellow': yellow,
})


def main():
	from txt import rgb
	for name, c in colors:
		print(rgb(name, *c))


if __name__ == '__main__':
	main()
