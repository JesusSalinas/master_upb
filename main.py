import json

from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.scrap import ParseHubScrap

# doc = {
#     'name': 'Carls Max',
#     'age': 30,
#     'email': 'carls_max@example.com'
# }

resources = {
    'uuid': '2624614',
    'date': '2024-04-20',
    'project_id': '23965969',
    'research_source': 'uk url',
    'txt_to_analyze': [

    ],
    'txt_analized': ''
}

projects = {
    'project_id': '',
    'name': 'rf',
    'started_date': 'fgr',
    'end_date': '',
    'finished': False,
    'author': '',
    'outcomes': [
        {
            'id': '',
            'data': ''
        }
    ]
}

outcomes = {
    'project_id': '',
}



txt = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
txt_eng = 'I love you like the sea loves the river, like the night loves the day, like the sun loves the moon, like light loves the day.'
# connector = AIOpenAPI()
# response = connector.prompt(txt_eng, 500)
# tx = response.choices[0].text.strip()
# #print(tx)
# resources['txt_analized'] = tx

# print(resources)

# print('\n')

# connector = MongoDBConnector()
# connector.connect()
# connector.get_collection('CollectionTest')

# if (connector.collection!=None):
#     connector.insert_document(resources)

# if (connector.collection!=None):
#     results = connector.collection.find({}) 
#     for result in results:
#         print(result)

# connector.disconnect()

# txt_to_analyze = get_txt_from_pdf('natural_language.pdf')
# textos_por_pagina = dividir_pdf('natural_language.pdf')
# primer_elemento = next(iter(textos_por_pagina.items()))
# txt_to_analyze = primer_elemento

connector = MongoDBConnector()
connector.connect()
connector.get_collection('CollectionTest')

scrap = ParseHubScrap()
info = scrap.get_all_projects()
projects = json.loads(info)

for project in projects['projects']: 
    if project['title'] == 'uk_gob':
        token = project['token']

if token is not None:
    info_project = scrap.run_project(token)
    run = json.loads(info_project)
    #print(run)
    run_token = run['run_token']
    print(run_token)
    info = scrap.run_status(run_token)
    info_run = json.loads(info)
   # print(info)
    while info_run['status'] != 'complete':
        info = scrap.run_status(run_token)
        info_run = json.loads(info)
        print('dentro')
    if info_run['status'] == 'complete':
        data = scrap.get_data_run(run_token)
        data_run = json.loads(data)
        resources['txt_to_analyze'].append(data_run)
        if (connector.collection!=None):
            connector.insert_document(resources)

if (connector.collection!=None):
    results = connector.collection.find({}) 
    for result in results:
        print(result)

connector.disconnect()


# obtenemos los projectos, guardamos en array mandamos ejecutarlos async
# y luego consultamos estatus guardanod la info

# y luego hacemos el analisis

# y luego?

#a = scrap.get_data_run('tRm2etJR1f5R')
#print(a)

#uk_gob

# https://www.gov.uk/government/organisations/environment-agency
# https://espanol.epa.gov/
# https://asogravas.org/



# import asyncio
# import aiohttp

# async def consultar_status(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return response.status

# async def main():
#     url = 'https://ejemplo.com'  # Reemplaza con tu URL de consulta
#     status = await consultar_status(url)
#     print(f"El estado de la consulta a {url} es: {status}")

# asyncio.run(main())