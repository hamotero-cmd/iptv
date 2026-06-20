import requests, re, gzip, xml.etree.ElementTree as ET
from datetime import datetime

FUENTES = {
    "TDT": "https://www.tdtchannels.com/lists/tv.m3u",
    "Pluto": "https://raw.githubusercontent.com/iptv-org/iptv/master/countries/es.m3u",
    "Espanol": "https://iptv-org.github.io/iptv/languages/spa.m3u",
}
EPGS = [
    "https://www.tdtchannels.com/epg.xml.gz",
    "https://iptv-org.github.io/epg/guides/es/pluto.tv.epg.xml.gz",
]

print("🎣 PESCANDO SIN TEST...")
salida = ['#EXTM3U url-tvg="https://raw.githubusercontent.com/hamotero-cmd/iptv/main/epg_fusion.xml"']
total=0
for nombre,url in FUENTES.items():
    try:
        txt = requests.get(url, timeout=30).text
        canales = re.findall(r'(#EXTINF[^\n]+\nhttps?://[^\n]+)', txt)
        for c in canales:
            salida.append(c)
            total+=1
        print(f"{nombre}: {len(canales)}")
    except Exception as e:
        print(f"Error {nombre}: {e}")

with open("lista_pro.m3u","w",encoding="utf-8") as f:
    f.write("\n".join(salida))

print("📺 EPG...")
root = ET.Element("tv")
for epg_url in EPGS:
    try:
        data = gzip.decompress(requests.get(epg_url, timeout=30).content)
        tree = ET.fromstring(data)
        for child in tree: root.append(child)
    except: pass
ET.ElementTree(root).write("epg_fusion.xml", encoding="utf-8", xml_declaration=True)

print(f"Listo - {total} canales")
