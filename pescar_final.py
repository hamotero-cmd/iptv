import requests, re, xml.etree.ElementTree as ET

FUENTES = {
    "TDT": "https://www.tdtchannels.com/lists/tv.m3u",
    "Pluto": "https://i.mjh.nz/PlutoTV/es.m3u8",
    "Espanol": "https://iptv-org.github.io/iptv/languages/spa.m3u",
}

def clasificar(nombre, grupo_original):
    n = (nombre + " " + grupo_original).lower()
    if any(x in n for x in ["cine","pelicula","pluto cine","accion","terror","comedia","drama","estelar"]): return "CINE"
    if any(x in n for x in ["serie","ficcion","novela"]): return "SERIES"
    if any(x in n for x in ["deport","futbol","laliga","golf","sport","dazn","eurosport"]): return "DEPORTES"
    if any(x in n for x in ["docu","historia","natur","ciencia","national geographic","discovery","odisea"]): return "DOCUMENTALES"
    if any(x in n for x in ["tdt","la 1","la1","la 2","antena","cuatro","telecinco","sexta","trece"]): return "TDT"
    return "GENERAL"

salida = ['#EXTM3U url-tvg="https://raw.githubusercontent.com/hamotero-cmd/iptv/main/epg_fusion.xml"']
vistos = set()

for nombre_fuente, url in FUENTES.items():
    try:
        txt = requests.get(url, timeout=30).text
        for linea in txt.splitlines():
            if linea.startswith("#EXTINF"):
                tvg_id = re.search('tvg-id="([^"]*)"', linea)
                logo = re.search('tvg-logo="([^"]*)"', linea)
                grupo = re.search('group-title="([^"]*)"', linea)
                nombre = linea.split(",")[-1].strip()
                
                nuevo_grupo = clasificar(nombre, grupo.group(1) if grupo else "")
                linea_nueva = f'#EXTINF:-1 tvg-id="{tvg_id.group(1) if tvg_id else ""}" tvg-logo="{logo.group(1) if logo else ""}" group-title="{nuevo_grupo}",{nombre}'
                salida.append(linea_nueva)
            elif linea.startswith("http") and "m3u8" in linea:
                if linea not in vistos:
                    salida.append(linea)
                    vistos.add(linea)
    except: pass

open("lista_pro.m3u","w",encoding="utf-8").write("\n".join(salida))
print(f"Lista reagrupada: {len([l for l in salida if l.startswith('http')])} canales")
