import os
from pytube import YouTube

savedir = os.getcwd() + '/yt'

def download(url: str):
    # initialize
    print(">>> initializing")
    print('url: ' + url)
    yt = YouTube(url)
    title = yt.title
    print('video title: ' + title)
    # config
    print('download to ' + savedir + '/' + title)
    print('>>> choose a stream to download:')
    streams = yt.streams
    for i in range(len(streams)):
        print('\t' + str(i) + '. ' + str(yt.streams[i]))
    choice = int(input('download stream: '))
    #
    print('>>> downloading...')
    streams[choice].download(savedir)


if __name__ == '__main__':
    while True:
        print(">>> Fill to process")
        url = input("URL: ")
        download(url)
        print(">>> completed\n")
