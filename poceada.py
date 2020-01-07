import requests
from bs4 import BeautifulSoup
import dateutil.parser as dparser

url = 'http://www1.loteria.chaco.gov.ar'

page = requests.get('http://www1.loteria.chaco.gov.ar/index.php/extractos/poceada')

soup = BeautifulSoup(page.text, 'html.parser')

sorteos = soup.find(class_='juegos')

sorteos = sorteos.find_all('a')

enlaces = []

for sorteo in sorteos:
    link = url + sorteo.get('href')
    enlaces.append(link)
#print(enlaces)

for enlace in enlaces:
    print("Analizando: " + enlace)
    pagina = requests.get(enlace)
    sopa = BeautifulSoup(pagina.text, 'html.parser')
    
    numero_de_sorteo = sopa.find(class_='sorteo').text
    fecha = sopa.find(class_='date').text
    
    numero_de_sorteo = [int(s) for s in numero_de_sorteo.split() if s.isdigit()]
    numero_de_sorteo_string = str(numero_de_sorteo)

    fecha = dparser.parse(fecha,fuzzy=True)
    fecha_string = fecha.strftime("%d/%m/%Y")

    print("Sorteo número :"+numero_de_sorteo_string+" del día: "+fecha_string)

    tabla = sopa.find(class_='pizarron')
    numeros = []
    filas = tabla.findAll('tr')
    for fila in filas:
        numero = fila.find('td')
        if not (numero is None):
            numero = numero.text
            numeros.append(numero)
    print(numeros)
