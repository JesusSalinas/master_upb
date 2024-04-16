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
    'uuid': '3634634',
    'date': '2024-04-14',
    'project_id': '67967969',
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


scrap = ParseHubScrap()
a = scrap.get_data_run('tRm2etJR1f5R')
#print(a)

# json_data = json.loads(run.text)
# print(json_data)

json_data = json.loads(a)
print(json_data)

# getRun = requests.get('https://www.parsehub.com/api/v2/runs/tGmVPjTvAvo9', params=params)
# json_data = json.loads(getRun.text)
# print(json_data)
# print(getRun.text)

# getData = requests.get('https://www.parsehub.com/api/v2/runs/tGmVPjTvAvo9/data', params=params)
# print(getData.text)


# https://www.gov.uk/government/organisations/environment-agency
# https://espanol.epa.gov/
# https://asogravas.org/