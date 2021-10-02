import os, threading

def play(f):
	os.system('cmd /c "mpv \"{}\""'.format(f))

if __name__ == '__main__':
	for f in open('compare.inp', 'r', encoding='utf-8'):
		threading.Thread(target=play, args=([f.rstrip()])).start()
