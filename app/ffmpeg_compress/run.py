import os
from datetime import date

def leave_note(folder):
	today = date.today()
	#
	f = open(os.path.join(folder, 'compressed.txt'), 'w')
	f.write('this folder was compressed by ffmpeg_compress on {}-{}-{} (YYYY-MM-DD)'.format(
		today.year, today.month, today.day
	))

def compress(folder, remove_when_done):
	src = os.path.join(folder, 'src')
	for f in os.listdir(src):
		try:
			os.system('cmd /c "ffmpeg -i \"{}\" \"{}\""'.format(
				os.path.join(src, f),
				os.path.join(folder, f)
			))
		except:
			continue
		if remove_when_done:
			os.remove(os.path.join(src, f))
	leave_note(folder)

def handle_line(folder, remove_when_done):
	if len(folder) > 0:
		try:
			compress(folder.rstrip(), remove_when_done)
		except:
			pass

def main():
	for folder in open('_inp\\keep_after_compress.inp', 'r', encoding='utf-8'):
		handle_line(folder, False)
	for folder in open('_inp\\delete_after_compress.inp', 'r', encoding='utf-8'):
		handle_line(folder, True)



if __name__ == '__main__':
	main()
	# os.system('cmd /c "shutdown /s /t 0"')
