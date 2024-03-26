import requests
from bs4 import BeautifulSoup
import json
import requests

params = {
  "api_key": "tnBavm0BZh2J",
  "format": "json"
}


# run = requests.post("https://www.parsehub.com/api/v2/projects/tYJCFXHyCta6/run", data=params)

# json_data = json.loads(run.text)
# print(json_data)

# getRun = requests.get('https://www.parsehub.com/api/v2/runs/tGmVPjTvAvo9', params=params)
# json_data = json.loads(getRun.text)
# print(json_data)
# print(getRun.text)

getData = requests.get('https://www.parsehub.com/api/v2/runs/tGmVPjTvAvo9/data', params=params)
print(getData.text)

# URL de la página a scrapear
# url = 'https://www.gov.uk/government/publications/uk-government-green-financing'

# # https://www.gov.uk/government/organisations/environment-agency
# # https://espanol.epa.gov/
# # https://asogravas.org/

# # Realizar la solicitud GET a la página
# response = requests.get(url)

# # Verificar si la solicitud fue exitosa (código de estado 200)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, "html.parser")
#     p_tags = soup.find_all("p")
#     #titles = [p.find("a").get_text() for p in p_tags]

#     print(p_tags)
# else:
#     print(f'Error al obtener la página. Código de estado: {response.status_code}')
#     print(response.reason)