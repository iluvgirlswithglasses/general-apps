import os

"""
aegisub style args[] {
	0: 	stylename
	1: 	fontname
	2: 	fontsize
	3: 	color/primary
	4: 	color/secondary
	5: 	color/outline
	6: 	color/shadow
	7: 	bold
	8: 	italic
	9: 	underline
	10:	strikeout
	11: scaleX
	12: scaleY
	13: spacing
	14: angle (rotation)
	15: borderstyle
	16: outline
	17: shadow
	18: alignment
	19: marginL
	20: marginR
	21: marginV
	22: encoding
}
"""
def modification(args):
	# you might want to change your subtrack here
	# all args must be string
	args[2] = str(
		int(0.75 * int(args[2]))
	)


style_prefix = 'Style: '
style_prefix_len = len(style_prefix)

def fixstyle(line):
	args = line[style_prefix_len:].rstrip().split(',')
	modification(args)
	return 'Style: {}\n'.format(','.join(args))

def fixtrack(folder, f):
	inp = open(os.path.join(folder, 'subtrack', f), 'r', encoding='utf-8')
	out = open(os.path.join(folder, f), 'w', encoding='utf-8')
	for line in inp:
		if line[0:style_prefix_len] == style_prefix:
			out.write(fixstyle(line))
		else:
			out.write(line)

def fixfolder(folder):
	for f in os.listdir(os.path.join(folder, 'subtrack')):
		fixtrack(folder, f)


if __name__ == '__main__':
	for f in open('fixsub.inp', 'r', encoding='utf-8'):
		fixfolder(f.rstrip())
