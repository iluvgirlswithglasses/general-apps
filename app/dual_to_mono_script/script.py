
# the first anime automated by this script:
# Higurashi no Naku koro ni

import os

def extract(f: str):
	# shell script to be executed:
	# 	mkvmerge -o "out.mkv" -a 2 -s 4 "inp.mkv"
	# in which 2 and 4 are chosen audio track id and subtitle track id
	# to see all tracks information, execute command:
	# 	mkvmerge --identify "inp.mkv"
	os.system(
		'cmd /c "mkvmerge -o \"{}\" -a 2 -s 4 \"{}\""'.format(f, 'dual/' + f)
	)


if __name__ == '__main__':
	for f in os.listdir('dual/'):
		extract(f)
