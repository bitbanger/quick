import re


def splitf(regex):
	def _(s):
		chunks = []
		buf = ''
		while s:
			match = re.search(regex, s, re.MULTILINE).group(0)
			if match and s.index(match)==0:
				if buf:
					chunks.append(buf)
					buf = ''
				chunks.append(match)
				s = s[len(match):]
			else:
				buf += s[0]
				s = s[1:]
		if buf:
			chunks.append(buf)
			buf = ''

		return chunks
	return _
