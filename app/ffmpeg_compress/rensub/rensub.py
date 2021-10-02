import os

l = len('_Track2.unknown')

def ren(folder):
	src = os.path.join(folder, "src")
	for f in os.listdir(src):
		ext = os.path.splitext(f)[1];
		if (ext == '.unknown'):
			os.rename(
				os.path.join(src, f),
				os.path.join(folder, f[0:len(f)-l] + '.ass')
			)

if __name__ == '__main__':
	for f in open('rensub.inp', 'r'):
		ren(f.rstrip())
