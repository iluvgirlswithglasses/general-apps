import os

src = 'D:\\.completed_apps\\powershell-exts'	# source .installation directory
des = 'H:\\completed_apps\\powershell-exts'	# destination .installation directory
exc = {'', }				# exclusion files

def fetch(folder: str):
	print(folder + ":")
	#
	fs = {'', }
	# get all files in this des subdir
	for f in os.listdir(os.path.join(des, folder)):
		fs.add(f)
	# compare them to the source
	for f in os.listdir(os.path.join(src, folder)):
		if f not in exc and f not in fs:
			print("\t" + f)
	print()

if __name__ == '__main__':
	# load exclusion
	for f in open('exclusion.txt', 'r', encoding='utf-8'):
		exc.add(f)
	#
	for folder in os.listdir(des):
		if os.path.isdir(os.path.join(des, folder)):
			fetch(folder)
