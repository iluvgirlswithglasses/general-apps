Get-ChildItem -recurse -include *.flac, *.wav, *.ogg, *.mka, *.webm, *.m4a, *.mp3, *.mkv, *.mp4 | ForEach-Object { $_.FullName } > _ls.txt
mpv -playlist='_ls.txt'
rm _ls.txt