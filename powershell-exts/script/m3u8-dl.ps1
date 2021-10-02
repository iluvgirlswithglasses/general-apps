$url=$args[0]
$out=$args[1]
ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i $url -c copy $out