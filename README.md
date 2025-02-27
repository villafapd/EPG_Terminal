Codigo elaborado en python 3.11 para leer desde la terminal de Raspberry pi4 las guias de programacion (EPG) de distintos sitios que son publicados en:
https://github.com/iptv-org/epg/tree/master
Luego de seguir todos los pasos de instalacion previa de Node.js y npm indicados en el sitio iptv-org/epg y finalmente probado todo el funcionamiento para la obtención de la guia EPG.
El codigo realiza:
1) Escaneo de varios sitios (nzxmltv.com, epgshare01.online(RAKUTEN_PL1,US1.channels,DISTROTV1.channels), directv.com.ar, cableplus.com.uy) que tienen la EPG (https://github.com/iptv-org/epg/tree/master/sites)
2) Luego del escaneo se generan varios archivos .xml (Guia_XXXXX.xml)
3) Se genera un reemplazo de caracteres especiales (Español) Ñ,ñ,á,é,í,ó,ú,Á,É,Í,Ó,Ú
4) Se genera un reemplazo de una cadana de texto por otra.
5) Se guarda toda la informacion de cada archivo xml generado en un archivo guide.xml
6) Se ejecuta el codigo a las 3 am automaticamente
