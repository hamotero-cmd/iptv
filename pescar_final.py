import requests, re, unicodedata, concurrent.futures, gzip, xml.etree.ElementTree as ET
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

def normaliza(t):
    t = unicodedata.normalize('NFKD', t.lower())
    return re.sub(r'[^a-z0-9]','', ''.join(c for c in t if not unicodedata.combining(c)))

def test_stream(url):
    try:
        r = requests.head(url, timeout=5, allow_redirects=True, headers={"User-Agent":"VLC/3.0"})
        return r.status_code < 400
    except:
        return False

print("🎣 PESCANDO...")
canales = []
for nombre,url in FUENTES.items():
    try:
        txt = requests.get(url, timeout=20).text
        for b in re.split(r'\n(?=#EXTINF)', txt):
            if "#EXTINF" not in b: continue
            lineas = b.strip().split("\n")
            url_stream = lineas[-1].strip()
            if not url_stream.startswith("http"): continue
            nom = re.search(r',([^,]+)$', lineas[0])
            nombre_canal = nom.group(1).strip() if nom else "?"
            canales.append({"bloque":b, "url":url_stream, "nombre":nombre_canal, "key":normaliza(nombre_canal)})
    except Exception as e:
        print(f"Error {nombre}: {e}")

# dedup
vistos=set(); unicos=[]
for c in canales:
    if c["key"] not in vistos:
        vistos.add(c["key"]); unicos.append(c)

print(f"🔍 Testeando {len(unicos)} streams...")
with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
    resultados = list(ex.map(lambda c: test_stream(c["url"]), unicos))

vivos = [c for c,r in zip(unicos,resultados) if r]
print(f"✅ Vivos: {len(vivos)}/{len(unicos)}")

# escribe M3U para GitHub
salida = ['#EXTM3U url-tvg="https://raw.githubusercontent.com/hamotero-cmd/iptv/main/epg_fusion.xml"']
for c in vivos: salida.append(c["bloque"])
with open("lista_pro.m3u","w",encoding="utf-8") as f:
    f.write("\n".join(salida))

# fusiona EPG
print("📺 Fusionando EPG...")
root = ET.Element("tv", attrib={"generator-info-name":"PezPadre"})
for epg_url in EPGS:
    try:
        data = requests.get(epg_url, timeout=30).content
        xml = gzip.decompress(data)
        tree = ET.fromstring(xml)
        for child in tree: root.append(child)
    except Exception as e:
        print(f"EPG error: {e}")

ET.ElementTree(root).write("epg_fusion.xml", encoding="utf-8", xml_declaration=True)

print(f"Listo {datetime.now()} - {len(vivos)} canales")
