import datetime
with open("lista_pro.m3u","w",encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"# Generado {datetime.datetime.utcnow()}\n")
    f.write('#EXTINF:-1,La 1 HD\n')
    f.write('https://rtve.es/live/la1.m3u8\n')
print("ok")
