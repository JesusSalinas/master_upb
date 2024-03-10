import requests
from bs4 import BeautifulSoup

# URL de la página a scrapear
url = 'https://espanol.epa.gov/'

# https://www.gov.uk/government/organisations/environment-agency
# https://espanol.epa.gov/
# https://asogravas.org/

# Realizar la solicitud GET a la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    p_tags = soup.find_all("p", "title")
    titles = [p.find("a").get_text() for p in p_tags]

    print(p_tags)
else:
    print(f'Error al obtener la página. Código de estado: {response.status_code}')
    print(response.reason)