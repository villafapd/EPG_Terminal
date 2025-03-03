import subprocess
import re
import schedule
import time
import setproctitle

setproctitle.setproctitle("EGP_Scanner")

# Rutas de los archivos
archivo1 = '/home/villafapd/Documents/epg/Guia_DirecTv.xml'
archivo2 = '/home/villafapd/Documents/epg/Guia_DistroTv.xml'
archivo3 = '/home/villafapd/Documents/epg/Guia_CablePlus.xml'
archivo4 = '/home/villafapd/Documents/epg/Guia_RAKUTEN_PL1.xml'
archivo5 = '/home/villafapd/Documents/epg/Guia_US1.xml'
archivo6 = '/home/villafapd/Documents/epg/Guia_nzxmltv.com.xml'
archivo7 = '/home/villafapd/Documents/epg/Guia_PlutoTv_Vevo.xml'
archivo_guide = '/home/villafapd/Documents/epg/guide.xml'

def armar_guide_xml():
	# Extraer lineas necesarias de cada archivo
	linea_xml = extraer_primera_linea_con_xml(archivo1)
	lineas_channel_1 = extraer_lineas_con_tag(archivo1, '<channel id=')
	lineas_channel_2 = extraer_lineas_con_tag(archivo2, '<channel id=')
	lineas_channel_3 = extraer_lineas_con_tag(archivo3, '<channel id=')
	lineas_channel_4 = extraer_lineas_con_tag(archivo4, '<channel id=')
	lineas_channel_5 = extraer_lineas_con_tag(archivo5, '<channel id=')
	lineas_channel_6 = extraer_lineas_con_tag(archivo6, '<channel id=')
	lineas_channel_7 = extraer_lineas_con_tag(archivo7, '<channel id=')
 
	lineas_programme_1 = extraer_lineas_con_tag(archivo1, '<programme start=')
	lineas_programme_2 = extraer_lineas_con_tag(archivo2, '<programme start=')
	lineas_programme_3 = extraer_lineas_con_tag(archivo3, '<programme start=')
	lineas_programme_4 = extraer_lineas_con_tag(archivo4, '<programme start=')
	lineas_programme_5 = extraer_lineas_con_tag(archivo5, '<programme start=')
	lineas_programme_6 = extraer_lineas_con_tag(archivo6, '<programme start=')
	lineas_programme_7 = extraer_lineas_con_tag(archivo7, '<programme start=')
	Linea_fin_xml = extraer_lineas_con_tag(archivo1, '</tv>')
 
	# Combinar todas las lineas en el orden requerido
	lineas_combined = [linea_xml] + lineas_channel_1 + lineas_channel_2 + lineas_channel_3 + lineas_channel_4 + lineas_channel_5 + lineas_channel_6 + lineas_channel_7 
	lineas_combined += lineas_programme_1 + lineas_programme_2 + lineas_programme_3 + lineas_programme_4 + lineas_programme_5 + lineas_programme_6 + lineas_programme_7 + Linea_fin_xml

	lineas_combined = reemplazar_caracteres_especiales_linea_por_linea(lineas_combined)
	lineas_combined = reemplazar_caracteres_especiales_linea_por_linea(lineas_combined)

	cadena_buscar = "DISTROTV1#beIN.SPORTS.Xtra.en.Español.distro"
	cadena_reemplazar = "beIN.SPORTS.Xtra.en.Espanol"
	reemplazar_cadena_en_lista(lineas_combined, cadena_buscar, cadena_reemplazar)	
 
	# Escribir las lineas combinadas en guide.xml
	with open(archivo_guide, 'w', encoding='utf-8') as file:
		for linea in lineas_combined:
			file.write(linea + '\n')

	print("Lineas copiadas y pegadas exitosamente en el archivo guide.xml")    

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

def ejecutar_comando(SITE,NOMBRE_ARCHIVO):    
	comando = f'bash -c \'cd /home/villafapd/Documents/epg && npm run grab --- --output="{NOMBRE_ARCHIVO}" --channels="{SITE}"\''

	proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	salida, error = proceso.communicate()

	# Verificar el estado de salida del proceso
	if proceso.returncode != 0:
		print(f"Error en la ejecucion del comando: {error.decode()}")
		return None

	return salida.decode(),SITE

def ejecutar_comando_site(SITE,NOMBRE_ARCHIVO):    
	comando = f'bash -c \'cd /home/villafapd/Documents/epg && npm run grab --- --output="{NOMBRE_ARCHIVO}" --site="{SITE}"\''

	proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	salida, error = proceso.communicate()

	# Verificar el estado de salida del proceso
	if proceso.returncode != 0:
		print(f"Error en la ejecucion del comando: {error.decode()}")
		return None

	return salida.decode(),SITE


def leer_salida_terminal(salida):
	lineas = salida.split('\n')
	for linea in lineas:
		if "found" in linea and "channel(s)" in linea:
			# Extraer el numero de canales usando una expresion regular
			numero_canales = re.search(r'found (\d+) channel\(s\)', linea).group(1)
			return int(numero_canales)

def buscar_epg():
	# Ejecutar los comandos y luego leer la salida
	#-----------------------------------------------------------------------------------------------
	print('Comenzando el escaneo de sitios EPG')
	print("Espere por favor mientras se realiza el escaneo de nzxmltv.com")
	#-----------------------------------------------------------------------------------------------
	salida, site = ejecutar_comando("npm run grab --- --output=Guia_PlutoTv_Vevo.xml --channels=sites/nzxmltv.com/nzxmltv.com_pluto.channels.xml","Guia_PlutoTv_Vevo.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}")
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------
	print("Espere por favor mientras se realiza el escaneo de RAKUTEN_PL1.channels")
	time.sleep(5)
	#-----------------------------------------------------------------------------------------------
	salida, site = ejecutar_comando("sites/epgshare01.online/epgshare01.online_RAKUTEN_PL1.channels.xml","Guia_RAKUTEN_PL1.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}")
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------
	print("Espere por favor mientras se realiza el escaneo de US1.channels")
	time.sleep(5)
	salida, site = ejecutar_comando("sites/epgshare01.online/epgshare01.online_US1.channels.xml","Guia_US1.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}")
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------
	print("Espere por favor mientras se realiza el escaneo de DISTROTV1.channels.xml")
	time.sleep(10)
	salida, site = ejecutar_comando("sites/epgshare01.online/epgshare01.online_DISTROTV1.channels.xml","Guia_DistroTv.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}")
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------
	print("Espere por favor mientras se realiza el escaneo de directv.com.ar")
	time.sleep(10)
	salida, site = ejecutar_comando_site("directv.com.ar","Guia_DirecTv.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacaion para {site}") 

	print("Espere por favor mientras se realiza el escaneo de cableplus.com.uy")
	time.sleep(10)
	salida, site = ejecutar_comando_site("cableplus.com.uy","Guia_CablePlus.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}") 
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------

	armar_guide_xml()

def buscar_epg_redbulltv():
	print("Espere por favor mientras se realiza el escaneo de nzxmltv.com")
	salida, site = ejecutar_comando("sites/nzxmltv.com/nzxmltv.com_redbull.channels.xml","Guia_nzxmltv.com.xml")
	if salida:
		numero_canales = leer_salida_terminal(salida)
		print(f"Guia descargada correctamente para los {numero_canales} canales del sitio {site}")
	else: 
		print(f"Error en la descarga de la Guia de programacion para {site}")
	#-----------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------
	armar_guide_xml()
	




if __name__ == "__main__":

# Programar la funcion para que se ejecute cada 6 horas
	#schedule.every(HorasEjecucion).hours.do(busca_url)
	schedule.every().day.at("02:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("05:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("07:00").do(buscar_epg)
	schedule.every().day.at("08:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("11:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("14:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("17:00").do(buscar_epg_redbulltv) 
	schedule.every().day.at("18:00").do(buscar_epg)
	schedule.every().day.at("20:00").do(buscar_epg_redbulltv)
	schedule.every().day.at("23:00").do(buscar_epg_redbulltv)
	
	#buscar_epg()
	try:
		while True:
			schedule.run_pending()
			time.sleep(5)
	except KeyboardInterrupt:
		print("Programa interrumpido. Limpiando recursos...")



