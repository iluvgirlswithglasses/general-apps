"""
If mikaKOn is upgraded to higher version,
It'll have multiple files, storing multiple class
However, in this version, it need to be finished quick
We need to finish what we started, ASAP
Only mikaDb can do the opposite
"""

from tkinter import Tk, Canvas, Scrollbar, StringVar, mainloop
from tkinter import ttk
import files
from pygame import mixer
from pydub import AudioSegment
from pydub.utils import mediainfo
from PIL import Image, ImageTk
import random


# noinspection PyUnusedLocal
class Window:
    """ the only window of mikaKOn """

    def __init__(self):
        """ initialize the window """
        """ root setup """
        self.root = Tk()
        self.root.minsize(880, 252)
        self.root.geometry("880x252")
        self.root.resizable(width=True, height=False)
        self.root.title("mikaKOn - K-On!")
        self.root.iconbitmap(files.ico_dir)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        """ operating vars """
        self.playlist = []
        self.songs_detail = []
        self.songs_length = []
        self.songs_label = []
        self.playing_index = -1
        self.playing_file = None  # this still use the file when mixer.quit() is call
        self.streaming = True
        self.volume = 0.8
        self.timer = None
        self.loop = False

        """ gridding """
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        """ browsing toolbar """
        # frame
        self.browse_toolbar = ttk.Frame(self.root, style="browse_toolbar.TFrame")
        self.browse_toolbar.grid(column=2, row=0, sticky="ew")
        # guides
        ttk.Label(self.browse_toolbar, text="Browse mode:", style="browse_guide.TLabel").grid(column=0, row=0)
        # modes
        self.browse_mode = StringVar()
        ttk.OptionMenu(self.browse_toolbar, self.browse_mode, "Files", style="browse_menu.TMenubutton",
                       *("Files", "Folder", "Folder and subfolders")).grid(column=1, row=0)
        # browses
        self.browse_bt = ttk.Label(self.browse_toolbar, text="browse ...", style="browse_bt.TLabel")
        self.browse_bt.grid(column=2, row=0)
        self.browse_bt.bind("<Button-1>", self.browse)

        """ infobox """
        # frame
        self.infobox = ttk.Frame(self.root, style="infobox.TFrame", width=600)
        self.infobox.grid_propagate(0)
        self.infobox.grid(column=2, row=1, sticky="nsew")
        # goddess
        goddess = self.gen_imagetk("goddess.png")
        goddess_canvas = Canvas(self.infobox, height=180, width=180, highlightthickness=0)
        goddess_canvas.create_image(0, 0, image=goddess, anchor="nw")
        goddess_canvas.image = goddess
        goddess_canvas.grid(column=0, row=0, rowspan=5, padx=(8, 24), pady=8)
        # labels
        wraplength = 600 - 180 - 8 - 24
        info_padx = (0, 24)
        self.infobox.grid_rowconfigure(0, weight=1)
        self.infobox_title = ttk.Label(self.infobox, text="", style="infobox_title.TLabel",
                                       anchor="w", wraplength=wraplength)
        self.infobox_title.grid(column=1, row=1, sticky="w", padx=info_padx)
        self.infobox_filename = ttk.Label(self.infobox, text="", style="infobox_filename.TLabel",
                                          anchor="w", wraplength=wraplength)
        self.infobox_filename.grid(column=1, row=2, sticky="w", padx=info_padx)
        self.infobox_filedir = ttk.Label(self.infobox, text="", style="infobox_filedir.TLabel",
                                         anchor="w", wraplength=wraplength)
        self.infobox_filedir.grid(column=1, row=3, sticky="w", padx=info_padx, pady=(12, 0))
        self.infobox.grid_rowconfigure(4, weight=1)

        """ controlbar operating bts """
        bt_padx = (12, 4)
        # frame
        self.controlbar = ttk.Frame(self.root, style="controlbar.TFrame", height=32)
        self.controlbar.grid(column=2, row=2, sticky="ew")
        self.controlbar.propagate(0)
        # bts
        self.play_pre_bt = self.gen_icon_bt("play-pre")
        self.play_pre_bt.grid(column=0, row=0, padx=bt_padx)
        self.play_next_bt = self.gen_icon_bt("play-next")
        self.play_next_bt.grid(column=1, row=0, padx=bt_padx)
        self.pause_bt = self.gen_pause_bt()
        self.pause_bt.grid(column=2, row=0, padx=bt_padx)
        self.replay_bt = self.gen_icon_bt("replay")
        self.replay_bt.grid(column=3, row=0, padx=bt_padx)
        # binding
        self.play_pre_bt.bind("<Button-1>", self.play_pre)
        self.play_next_bt.bind("<Button-1>", self.play_next)
        self.replay_bt.bind("<Button-1>", self.replay)

        """ controlbar slider """
        self.controlbar.grid_columnconfigure(4, weight=1)
        # frame
        self.controlbar.grid_columnconfigure(4, weight=1)

        """ controlbar volume """
        self.volume_label = ttk.Label(self.controlbar, text="80", style="volume.TLabel", width=3, anchor="e")
        self.volume_label.grid(column=5, row=0, padx=(0, 2))
        # bts
        self.volume_down_bt = self.gen_volume_bt("volume-down")
        self.volume_down_bt.grid(column=6, row=0, padx=2)
        self.volume_up_bt = self.gen_volume_bt("volume-up")
        self.volume_up_bt.grid(column=7, row=0, padx=(2, 4))
        # bindings
        self.volume_down_bt.bind("<Button-1>", self.decrease_volume)
        self.volume_up_bt.bind("<Button-1>", self.increase_volume)

        """ playlist toolbar """
        # playlist toolbar
        self.playlist_toolbar = ttk.Frame(self.root, style="playlist_toolbar.TFrame")
        self.playlist_toolbar.grid(column=0, columnspan=2, row=0, sticky="ew")
        self.playlist_toolbar.grid_columnconfigure(2, weight=1)
        # shuffle bt
        self.shuffle_bt = ttk.Label(self.playlist_toolbar, text="Shuffle", style="playlist_toolbar.TLabel")
        self.shuffle_bt.grid(column=0, row=0, sticky="w")
        self.shuffle_bt.bind("<Button-1>", self.on_shuffle_bt_click)
        self.shuffle_bt.bind("<ButtonRelease-1>", self.on_shuffle_bt_out)
        # loop bt
        self.loop_bt = ttk.Label(self.playlist_toolbar, text="Loop", style="playlist_toolbar.TLabel")
        self.loop_bt.grid(column=1, row=0, sticky="w")
        self.loop_bt.bind("<Button-1>", self.on_loop_bt_change)
        # disp mode
        self.disp_mode = StringVar()
        ttk.OptionMenu(self.playlist_toolbar, self.disp_mode, "Title", style="playlist_toolbar.TMenubutton",
                       *["Title", "Filename"]).grid(column=2, row=0, sticky="e", padx=[0, 24])

        """ playlist box """
        # canvas & scrollbar
        self.playlist_canvas = Canvas(self.root, background="#666666", highlightthickness=0)
        self.playlist_canvas.grid(column=0, row=1, rowspan=2, sticky="nsew")
        self.playlist_scrollbar = Scrollbar(self.root, orient="vertical", command=self.playlist_canvas.yview)
        self.playlist_canvas.config(yscrollcommand=self.playlist_scrollbar.set)
        self.playlist_scrollbar.grid(column=1, row=1, rowspan=2, sticky="nse")
        # frame
        self.playlist_frame = ttk.Frame(self.playlist_canvas, style="playlist_frame.TFrame")
        self.playlist_frame_incanvas = self.playlist_canvas.create_window(0, 0, window=self.playlist_frame)
        # bindinds
        self.playlist_view_reset = True  # if this is True on self.playlist_frame configuration, view will be reset
        self.playlist_canvas.bind("<Configure>", self.on_playlist_canvas_configure)
        self.playlist_frame.bind("<Configure>", self.on_playlist_frame_configure)
        self.root.bind("<MouseWheel>", self.playlist_mousescroll)

    """ Browsing functions """
    def browse(self, *args):
        """ browsing interface """
        mapper = {
            "Files": files.browse_files,
            "Folder": files.browse_folder,
            "Folder and subfolders": files.browse_folders,
        }
        old_len = len(self.playlist)
        res = mapper[self.browse_mode.get()]()
        if len(res) == 0:
            return
        # if an imported song is needed to play instantly
        if self.playing_index == old_len - 1:
            self.playlist_append(res.pop(0))
            if self.streaming and mixer.music.get_pos() == -1:
                self.play_next()
        # the res
        for file in res:
            self.playlist_append(file)

    """ playlist """
    def playlist_append(self, file):
        self.playlist.append(file)
        detail = mediainfo(file.filedir)
        try:
            tags = detail['TAG']
            title = tags['title']
            self.songs_detail.append({'title': title})
        except:
            self.songs_detail.append({'title': file.filename})
        self.songs_length.append(int(float(detail['duration']) * 1000))
        self.playlist_frame_append(len(self.playlist) - 1)

    def playlist_frame_append(self, index):
        disp = self.songs_detail[index]['title']
        label = ttk.Label(self.playlist_frame, text="{}. {}".format(index+1, disp),
                          style="playlist_entry{}.TLabel".format(index % 2))
        label.bind("<Button-1>", lambda event, i=index: self.play_song(i))
        label.bind("<Button-3>", lambda event, i=index: self.del_song(i))
        label.pack(side="top", fill="x")
        self.songs_label.append(label)

    """ Timer functions """
    def del_song(self, index, *args):
        self.songs_detail.pop(index)
        self.playlist.pop(index)
        self.songs_length.pop(index)
        # this should be at the bottom, however
        # we need to reload the song if neccessary ASAP
        if index == self.playing_index:
            if len(self.playlist) > 0:
                self.play_song(index)
            else:
                self.playing_index -= 1
        # del labels that behind the index
        while len(self.songs_label) - 1 >= index:
            self.songs_label[index].destroy()
            self.songs_label.pop(index)
        # replaced the deleted with this
        for i in range(index, len(self.playlist)):
            self.playlist_frame_append(i)
        # index position handling
        if index < self.playing_index:
            self.playing_index -= 1
            self.songs_label[self.playing_index].config(foreground='#fc6104', font=('Calibri', '10', 'bold'))

    def set_timer(self, start=0):
        """ only call timer if playing command is shot """
        self.cancel_timer()

        def recursion(*args):
            if mixer.music.get_pos() == -1:
                self.play_next()
            else:
                self.timer = self.root.after(
                    64, recursion
                )

        self.timer = self.root.after(
            64, recursion
        )

    def cancel_timer(self):
        try:
            self.root.after_cancel(self.timer)
        except ValueError:
            pass

    """ volume functions """
    def decrease_volume(self, *args):
        self.set_volume(-0.2)

    def increase_volume(self, *args):
        self.set_volume(0.2)

    def set_volume(self, delta):
        self.volume += delta
        if self.volume > 1:
            self.volume = 1
        if self.volume < 0:
            self.volume = 0
        mixer.music.set_volume(self.volume)
        self.volume_label.config(text=int(self.volume * 100))

    """ Operating functions """
    def play_next(self, *args):
        if self.playing_index + 1 <= len(self.playlist) - 1:
            self.play_song(self.playing_index + 1)
        elif len(self.playlist) > 0 and self.loop:
            self.play_song(0)

    def play_pre(self, *args):
        if len(self.playlist) > 0 and self.playing_index - 1 > 0:
            self.play_song(self.playing_index - 1)

    def replay(self, *args):
        if len(self.playlist) == 0:
            return
        self.play_song(self.playing_index)
        self.set_timer()

    def shuffle(self):
        def swap(m, n):
            for lst in [self.playlist, self.songs_detail, self.songs_length]:
                lst.insert(n, lst.pop(m))
        # handle currently playing
        swap(self.playing_index, 0)
        self.playing_index = 0
        # others
        for i in reversed(range(
            2, len(self.playlist)
        )):
            swap(i, random.randint(1, i))
        # update playlistbox
        for i in self.songs_label:
            i.destroy()
        self.songs_label = []
        for i in range(len(self.playlist)):
            self.playlist_frame_append(i)
        self.playlist_view_reset = True
        self.songs_label[0].config(foreground='#fc6104', font=('Calibri', '10', 'bold'))

    """ Playing functions """
    def play_song(self, index):
        """ this function will modify self.playing_index """
        self.del_playing()
        if len(self.playlist) > 0:
            self.songs_label[self.playing_index].config(foreground='#000000', font=('Calibri', '10'))
        self.playing_index = index
        self.songs_label[self.playing_index].config(foreground='#fc6104', font=('Calibri', '10', 'bold'))
        self.load_song(index)
        mixer.music.play()
        if self.streaming:
            self.set_timer()
        else:
            mixer.music.pause()

    def load_song(self, index):
        file = self.playlist[index]
        self.infobox_title.config(text=self.songs_detail[index]['title'])
        self.infobox_filename.config(text=file.filename)
        self.infobox_filedir.config(text=file.filedir)
        audio = AudioSegment.from_file(file.filedir, file.filetype)
        mixer.pre_init(frequency=audio.frame_rate)
        audio.export(
            files.path_join(files.playing_dir, "playing.wav"), "wav"
        )  # export for last at setting up
        self.playing_file = open(files.playing_file)
        mixer.music.load(self.playing_file)

    """ Event functions """
    def on_loop_bt_change(self, *args):
        if self.loop:
            self.loop = False
            self.loop_bt.config(foreground="#dddddd")
        else:
            self.loop = True
            self.loop_bt.config(foreground="#fc6104")

    def on_shuffle_bt_click(self, *args):
        self.shuffle_bt.config(foreground='#fc6104')
        self.shuffle()

    def on_shuffle_bt_out(self, *args):
        self.shuffle_bt.config(foreground='#dddddd')

    def on_close(self, *args):
        self.root.destroy()
        mixer.quit()
        if self.playing_file is not None:
            self.playing_file.close()
        files.del_playing()

    def on_playlist_canvas_configure(self, *args):
        self.playlist_canvas.itemconfig(
            self.playlist_frame_incanvas, width=self.playlist_canvas.winfo_width()
        )

    def on_playlist_frame_configure(self, *args):
        if self.playlist_frame.winfo_height() <= self.playlist_canvas.winfo_height():
            self.playlist_canvas.moveto(self.playlist_frame_incanvas, 0, 0)
        self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox("all"))
        if self.playlist_view_reset:
            self.playlist_canvas.moveto(self.playlist_frame_incanvas, 0, 0)
            self.playlist_canvas.moveto(self.playlist_frame_incanvas, 0, 0)
            self.playlist_view_reset = False

    """ handling functions """
    def gen_icon_bt(self, filename):
        filedir = files.path_join(files.resource_dir, "bt", filename + ".png")
        pic = ImageTk.PhotoImage(Image.open(
            filedir
        ))
        canvas = Canvas(self.controlbar, width=32, height=32, highlightthickness=0, background="#fc6104")
        image = canvas.create_image(32 / 2, 32 / 2, image=pic)  # do not use anchor here
        canvas.image = pic
        return canvas

    def gen_volume_bt(self, filename):
        pic = self.gen_imagetk("bt", filename + ".png")
        canvas = Canvas(self.controlbar, width=16, height=32, highlightthickness=0, background="#fc6104")
        image = canvas.create_image(16 / 2, 32 / 2, image=pic)  # do not use anchor here
        canvas.image = pic
        return canvas

    def gen_pause_bt(self):
        # functions
        def pause(img, *args):
            # proc
            mixer.music.pause()
            self.streaming = False
            self.cancel_timer()
            # canvas
            canvas.delete(img)
            img = canvas.create_image(32 / 2, 32 / 2, image=pausing_icon)
            canvas.image = pausing_icon
            canvas.bind("<Button-1>", lambda *args: unpause(img))

        def unpause(img, *args):
            # proc
            mixer.music.unpause()
            self.streaming = True
            self.set_timer()
            # canvas
            canvas.delete(img)
            img = canvas.create_image(32 / 2, 32 / 2, image=streaming_icon)
            canvas.image = pausing_icon
            canvas.bind("<Button-1>", lambda *args: pause(img))

        # pausing / unpause bt icon
        streaming_icon = self.gen_imagetk("bt", "streaming.png")
        pausing_icon = self.gen_imagetk("bt", "pausing.png")
        # canvas
        canvas = Canvas(self.controlbar, width=32, height=32, highlightthickness=0, background="#fc6104")
        image = canvas.create_image(32 / 2, 32 / 2, image=streaming_icon)
        canvas.image = streaming_icon
        canvas.bind("<Button-1>", lambda *args: pause(image))

        return canvas

    @staticmethod
    def gen_imagetk(*args):
        filedir = files.path_join(files.resource_dir, *args)
        pic = ImageTk.PhotoImage(file=filedir)
        return pic

    def del_playing(self):
        try:
            mixer.music.stop()
            self.playing_file.close()
            files.del_playing()
        except AttributeError:
            pass

    def playlist_mousescroll(self, event):
        if self.playlist_frame.winfo_height() > self.playlist_canvas.winfo_height():
            if self.playlist_frame.winfo_y() + event.delta <= 0:
                self.playlist_canvas.move(self.playlist_frame_incanvas, 0, event.delta)
            elif self.playlist_frame.winfo_y() + event.delta >= -self.playlist_frame.winfo_height() \
                    + self.playlist_canvas.winfo_height():
                self.playlist_canvas.move(self.playlist_frame_incanvas, 0, event.delta)
            else:
                self.playlist_canvas.moveto(self.playlist_frame_incanvas, 0, 0)
        else:
            pass


if __name__ == "__main__":
    """ gen window """
    window = Window()
    mixer.init()
    mixer.music.set_volume(window.volume)

    """ styles """
    # browsing toolbar
    ttk.Style().configure("browse_toolbar.TFrame", background="#bbbbbb")
    ttk.Style().configure("browse_guide.TLabel", background="#bbbbbb", padding="12 0 4 0", font=("Calibri", "10"))
    ttk.Style().configure("browse_menu.TMenubutton", background="#bbbbbb", font=("Calibri", "10", "bold"))
    ttk.Style().configure("browse_bt.TLabel", background="#bbbbbb", foreground="#fc6104",
                          padding="12 0 4 0", font=("Calibri", "10", "bold"))
    # infobox
    ttk.Style().configure("infobox.TFrame", background="#dddddd", width=100)
    ttk.Style().configure("infobox_title.TLabel", background="#dddddd", foreground="#fc6104",
                          font=("Calibri Light", "20"))
    ttk.Style().configure("infobox_filename.TLabel", background="#dddddd", foreground="#00b050",
                          font=("Calibri Light", "12", "bold"))
    ttk.Style().configure("infobox_filedir.TLabel", background="#dddddd", foreground="#777777",
                          font=("Calibri", "10"))
    # controlbar
    ttk.Style().configure("controlbar.TFrame", background="#fc6104")
    ttk.Style().configure("volume.TLabel", background="#fc6104", foreground="#ffffff", font=("Calibri", "14", "bold"))
    # playlist toolbar
    ttk.Style().configure("playlist_toolbar.TFrame", background="#444444")
    ttk.Style().configure("playlist_toolbar.TLabel", foreground="#dddddd", background="#444444", padding="12 0 4 0",
                          font=("Calibri", "10", "bold"), highlightthickness=0)
    ttk.Style().configure("playlist_toolbar.TMenubutton", background="#444444", foreground="#fc6104",
                          font=("Calibri", "10", "bold"))
    # playlist
    ttk.Style().configure("playlist_frame.TFrame", background="#666666")
    ttk.Style().configure("playlist_entry0.TLabel", background="#777777")
    ttk.Style().configure("playlist_entry1.TLabel", background="#888888")

    """ mainloop """
    mainloop()
