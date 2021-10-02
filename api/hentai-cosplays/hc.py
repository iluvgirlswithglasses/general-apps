import os
#
import requests
import shutil

def requests_conn(src, des):
    r = requests.get(src, stream=True, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})
    if r.status_code == 200:
        with open(des, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        print("Successfully writen to ", des)
    else:
        print("Failed with code ", r.status_code, " - src: ", src)


#
if __name__ == '__main__':
    shift = int(input("shift: "))
    quan = input("pics count: ")
    link = input("link: ")
    savedir = input("save dir: ")
    ext = "png"
    for i in range(int(quan)):
        if not os.path.exists(os.path.join(savedir, "{}.jpg".format(i + shift, ext))):
            requests_conn(
                "{}/{}.{}".format(link, i + shift, ext),
                os.path.join(savedir, "{}.{}".format(i + shift, ext))
            )
