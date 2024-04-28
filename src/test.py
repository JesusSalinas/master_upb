import json

from src.mongo import MongoDBConnector
from src.scrap import ParseHubScrap

resources = {
    'uuid': '2624614',
    'date': '2024-04-20',
    'project_id': '23965969',
    'research_source': 'uk url',
    'txt_raw': [

    ],
    'txt_to_analyze': [

    ],
    'txt_analized': ''
}


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

# obtenemos los projectos, guardamos en array mandamos ejecutarlos async
# y luego consultamos estatus guardanod la info

# y luego hacemos el analisis

# y luego?


# txt = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
# txt_eng = 'I love you like the sea loves the river, like the night loves the day, like the sun loves the moon, like light loves the day.'
# connector = AIOpenAPI()
# response = connector.prompt(txt_eng, 500)
# tx = response.choices[0].text.strip()
# #print(tx)
# resources['txt_analized'] = tx

# print(resources)

# print('\n')


# https://www.gov.uk/government/organisations/environment-agency
# https://espanol.epa.gov
# https://asogravas.org



    # if archivo:
    #     try:
    #         with open(archivo, 'r') as f:
    #             lector_csv = csv.reader(f)
    #             contenido = ""
    #             for fila in lector_csv:
    #                 contenido += ", ".join(fila) + "\n"
    #             self.texto_contenido.delete("1.0", tk.END)
    #             self.texto_contenido.insert(tk.END, contenido)
    #     except Exception as e:
    #         tk.messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")