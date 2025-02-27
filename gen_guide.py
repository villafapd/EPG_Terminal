def reemplazar_cadena_en_lista(lista_texto, cadena_buscar, cadena_reemplazar):
    for i, linea in enumerate(lista_texto):
        if cadena_buscar in linea:
            lista_texto[i] = linea.replace(cadena_buscar, cadena_reemplazar)
    return lista_texto


def reemplazar_caracteres_especiales_linea_por_linea(lista_texto):
    if not isinstance(lista_texto, list):
        raise ValueError("El argumento 'lista_texto' debe ser una lista de cadenas de caracteres (list[str | None])")

    reemplazos = {
        'Ñ': 'N', 'ñ': 'n',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
    }

    texto_modificado = []

    for linea in lista_texto:
        if linea is not None:
            linea_modificada = ''.join(reemplazos.get(c, c) for c in linea)
            texto_modificado.append(linea_modificada)
        else:
            texto_modificado.append(None)

    return texto_modificado





def extraer_lineas_con_tag(file_path, tag):
    lineas = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if tag in line:
                lineas.append(line.strip())
    return lineas

def extraer_primera_linea_con_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "<?xml" in line:
                return line.strip()
    return None



# Rutas de los archivos
archivo1 = '/home/villafapd/Documents/epg/Guia_DirecTv.xml'
archivo2 = '/home/villafapd/Documents/epg/Guia_DistroTv.xml'
archivo3 = '/home/villafapd/Documents/epg/Guia_CablePlus.xml'
archivo4 = '/home/villafapd/Documents/epg/Guia_RAKUTEN_PL1.xml'
archivo5 = '/home/villafapd/Documents/epg/Guia_US1.xml'
archivo6 = '/home/villafapd/Documents/epg/Guia_nzxmltv.com.xml'
archivo_guide = '/home/villafapd/Documents/epg/guide.xml'

# Extraer lineas necesarias de cada archivo
linea_xml = extraer_primera_linea_con_xml(archivo1)
lineas_channel_1 = extraer_lineas_con_tag(archivo1, '<channel id=')
lineas_channel_2 = extraer_lineas_con_tag(archivo2, '<channel id=')
lineas_channel_3 = extraer_lineas_con_tag(archivo3, '<channel id=')
lineas_channel_4 = extraer_lineas_con_tag(archivo4, '<channel id=')
lineas_channel_5 = extraer_lineas_con_tag(archivo5, '<channel id=')
lineas_channel_6 = extraer_lineas_con_tag(archivo6, '<channel id=')

lineas_programme_1 = extraer_lineas_con_tag(archivo1, '<programme start=')
lineas_programme_2 = extraer_lineas_con_tag(archivo2, '<programme start=')
lineas_programme_3 = extraer_lineas_con_tag(archivo3, '<programme start=')
lineas_programme_4 = extraer_lineas_con_tag(archivo4, '<programme start=')
lineas_programme_5 = extraer_lineas_con_tag(archivo5, '<programme start=')
lineas_programme_6 = extraer_lineas_con_tag(archivo6, '<programme start=')
Linea_fin_xml = extraer_lineas_con_tag(archivo1, '</tv>')

# Combinar todas las l�neas en el orden requerido
lineas_combined = [linea_xml] + lineas_channel_1 + lineas_channel_2 + lineas_channel_3 + lineas_channel_4 + lineas_channel_5 +lineas_channel_6
lineas_combined += lineas_programme_1 + lineas_programme_2 + lineas_programme_3 + lineas_programme_4 + lineas_programme_5 + lineas_programme_6 + Linea_fin_xml
lineas_combined = reemplazar_caracteres_especiales_linea_por_linea(lineas_combined)



cadena_buscar = "DISTROTV1#beIN.SPORTS.Xtra.en.Español.distro"
cadena_reemplazar = "beIN.SPORTS.Xtra.en.Espanol"

reemplazar_cadena_en_lista(lineas_combined, cadena_buscar, cadena_reemplazar)

# Escribir las lineas combinadas en guide.xml
with open(archivo_guide, 'w', encoding='utf-8') as file:
    for linea in lineas_combined:
        file.write(linea + '\n')

print("Lineas copiadas y pegadas exitosamente en el archivo guide.xml")
