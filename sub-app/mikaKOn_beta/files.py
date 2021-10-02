import os
from tkinter import filedialog

ico_dir = os.path.join("resource", "icon.ico")
playing_dir = os.path.join("playing")
playing_file = os.path.join(playing_dir, 'playing.wav')
resource_dir = os.path.join("resource")
supported = (".flac", ".wav", ".mp3", ".ogg", ".m4a")


class File:
    def __init__(self, filedir):
        self.filedir = filedir
        self.filename = os.path.basename(filedir)
        splt = os.path.splitext(self.filename)
        self.basename = splt[0]
        self.tail = splt[1]
        self.filetype = self.tail[1:]


def browse_files():
    res = []
    for file in filedialog.askopenfilenames(initialdir="\\", title="Choose file(s)",
                                            filetype=[(
                                                    "Supported audio files", supported,
                                            )]):
        res.append(File(
            os.path.normpath(file)
        ))
    return res


def browse_folder():
    res = []
    chosen_dir = os.path.normpath(
        filedialog.askdirectory(initialdir="\\", title="Choose folder")
    )
    if chosen_dir == '':
        return res
    for entry in os.listdir(chosen_dir):
        cr = os.path.join(chosen_dir, entry)
        if os.path.isfile(cr):
            file = File(cr)
            if file.tail in supported:
                res.append(file)
    return res


def browse_folders():
    res = []
    chosen_dir = os.path.normpath(
        filedialog.askdirectory(initialdir="\\", title="Choose folder")
    )
    if chosen_dir == '':
        return res

    def recursion(folder):
        for entry in os.listdir(folder):
            cr = os.path.join(folder, entry)
            if os.path.isdir(cr):
                recursion(cr)
            else:
                file = File(cr)
                if file.tail in supported:
                    res.append(file)

    recursion(chosen_dir)
    return res


def path_join(path, *args):
    return os.path.join(path, *args)

def del_playing():
    if os.path.exists(playing_file):
        os.remove(playing_file)
