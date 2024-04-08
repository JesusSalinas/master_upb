from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI

connector = MongoDBConnector()
connector.connect()
connector.get_collection('CollectionTest')

if (connector.collection!=None):
    results = connector.collection.find({}) 
    for result in results:
        print(result)

connector.disconnect()

txt = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
connector = AIOpenAPI()
response = connector.prompt(txt, 500)
print(response.choices[0].text.strip())



# txt_to_analyze = get_txt_from_pdf('natural_language.pdf')
# textos_por_pagina = dividir_pdf('natural_language.pdf')
# primer_elemento = next(iter(textos_por_pagina.items()))
# txt_to_analyze = primer_elemento