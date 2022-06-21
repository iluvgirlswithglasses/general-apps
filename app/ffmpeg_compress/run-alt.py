import os
from datetime import date

# config everything at line 19

def leave_note(folder):
	today = date.today()
	#
	f = open(os.path.join(folder, 'compressed.txt'), 'w')
	f.write('this folder was compressed by ffmpeg_compress on {}-{}-{} (YYYY-MM-DD)'.format(
		today.year, today.month, today.day
	))

def compress(audio_stream, subtitle_stream, folder, remove_when_done):
	src = os.path.join(folder, 'src')
	for f in sorted(os.listdir(src)):
		try:
			# config things here
			os.system('ffmpeg -i \"{}\" -map 0:v:0 -map 0:a:{} -map 0:s:{} -c:s copy \"{}\"'.format(
				os.path.join(src, f),
				audio_stream,
				subtitle_stream,
				os.path.join(folder, f)
			))
		except:
			continue
		else:
			if remove_when_done:
				os.remove(os.path.join(src, f))
	leave_note(folder)

def handle_line(line, remove_when_done):
	line = line.rstrip()
	if len(line) > 0:
		try:
			args = line.split("\\")
			compress(args[0], args[1], args[2], remove_when_done)
		except:
			pass

def main():
	# each line in these folder are written in this format:
	# {audio-stream}\{subtitle-stream}\{directory location}

	# files here are kept after compression
	for line in open('inp/keep-alt.inp', 'r', encoding='utf-8'):
		handle_line(line, False)
	# files here are deleted after compression
	for line in open('inp/del-alt.inp', 'r', encoding='utf-8'):
		handle_line(line, True)



if __name__ == '__main__':
	main()
	# os.system('shutdown 0')
