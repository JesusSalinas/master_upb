import fitz
import PyPDF2

def get_txt_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_doc:
        for num_page in range(pdf_doc.page_count):
            page = pdf_doc[num_page]
            text += page.get_text()
    return text

pdf_path = 'natural_language.pdf'

def dividir_pdf(input_path, max_palabras=4000):
    with open(input_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        textos = {}

        for page_num in range(len(pdf_reader.pages)):  # Utiliza len(reader.pages) en lugar de reader.numPages
            page = pdf_reader.pages[page_num]
            texto = page.extract_text()

            # Divide el texto en segmentos de no más de max_palabras palabras
            segmentos = [texto[i:i + max_palabras] for i in range(0, len(texto), max_palabras)]
            textos[f'pagina_{page_num + 1}'] = segmentos

    return textos


txt_to_analyze = get_txt_from_pdf(pdf_path)

# with open('resultado.txt', 'w', encoding='utf-8') as archivo_resultado:
#     archivo_resultado.write(txt_to_analyze)


textos_por_pagina = dividir_pdf(pdf_path)


# for pagina, segmentos in textos_por_pagina.items():
#     print(f"Página {pagina}:")
#     for i, segmento in enumerate(segmentos):
#         print(f"  Segmento {i + 1}: {segmento}")

primer_elemento = next(iter(textos_por_pagina.items()))
print(primer_elemento)

