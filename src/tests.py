from openai import OpenAI
from src.getPDF import get_txt_from_pdf, dividir_pdf

client = OpenAI(
    organization='org-SNspvMleh5EHgwB92bJrEujZ'
)

# txt_to_analyze = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
# txt_to_analyze = get_txt_from_pdf('natural_language.pdf')

textos_por_pagina = dividir_pdf('natural_language.pdf')
primer_elemento = next(iter(textos_por_pagina.items()))
txt_to_analyze = primer_elemento

response = client.completions.create(
  model="gpt-3.5-turbo-instruct",
  prompt=f"Analiza el siguiente texto: {txt_to_analyze}",
  max_tokens=500
)

print(response.choices[0].text.strip())