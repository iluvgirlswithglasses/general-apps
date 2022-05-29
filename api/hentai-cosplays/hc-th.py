import os
import threading
#
import urllib.request
#
import requests
import shutil

exts = ['.jpg', '.png', '.jpeg', '.webp']

# funcs
def urllib_conn(src, des):
    urllib.request.urlretrieve(src, des)

def change_ext(s, i):
    s = os.path.splitext(s)
    return s[0] + exts[i]

def requests_conn(src, des, i):
    if os.path.exists(des): return
    r = requests.get(src, stream=True, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'})
    if r.status_code == 200:
        with open(des, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print("Successfully writen to ", des)
    else:
        if i < len(exts) - 1:
            requests_conn(change_ext(src, i + 1), change_ext(des, i + 1), i + 1)
        else:
            print("Failed with code ", r.status_code, " - src: ", src)


#
if __name__ == '__main__':
    link = input("link regex: ")    # eg: https://static13.hentai-img.com/upload/20211031/796/814109/{}.jpg
    shift = int(input("shift: "))
    quan = input("pics count: ")
    savedir = input("save dir: ")
    #
    for i in range(int(quan)):
        th = threading.Thread(target=requests_conn, args=(
            link.format(i + shift),
            os.path.join(savedir, "{}.jpg".format(i + shift)),
            0
        ))
        th.start()
