#!/usr/bin/env python3
# pescar_final.py - version GitHub Actions
# Genera lista_pro.m3u con canales FTA (ejemplo simplificado)
import datetime

# Aquí va tu lógica real. Por ahora genera cabecera + ejemplo
channels = [
    "#EXTINF:-1 tvg-id="La1.es" tvg-logo="https://pbs.twimg.com/profile_images/123.png" group-title="España",La 1",
    "https://rtve.es/directo/la-1.m3u8",
    "#EXTINF:-1 tvg-id="BBCNews.uk" group-title="UK",BBC News",
    "https://vs-hls-push-uk.live.example/bbc.m3u8",
]

header = f"#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/es.xml"
# Generado: {datetime.datetime.utcnow().isoformat()}Z
"

with open("lista_pro.m3u", "w", encoding="utf-8") as f:
    f.write(header)
    f.write("
".join(channels))
    f.write("
")

print("lista_pro.m3u generado con", len(channels)//2, "canales")
