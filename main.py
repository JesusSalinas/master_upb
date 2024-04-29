import json
import tkinter as tk
import csv
import asyncio
import copy

from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.beauty import BeautySoapScrap
from src.interfaces import resources, projects, outcomes
from tkinter import filedialog

async def add_txt_raw():
    urls = projects['hosts']
    for link in urls:
        host = await scrap.valid_host(link)
        if host:
            resources['txt_raw'].append(copy.deepcopy(scrap.body))
        else: 
            txt_urls.insert(tk.END, 'Por favor validar la información del archivo. Error: ' + scrap.err + '\n')
            print(scrap.err)
    if resources['txt_raw']:
        connector = MongoDBConnector()
        connector.connect()
        connector.get_collection('CollectionTest')
        if (connector.collection!=None):
            connector.insert_document(resources)
            lab_get_txt.config(text='Información obtenida correctamente.')
    else: 
        lab_get_txt.config(text='Error al obtener la información. Por favor valida que las URL\'s se agregaron correctamente. ')

def get_urls_csv():
    urls= []
    file = filedialog.askopenfilename(initialdir="/", title="Selecciona un archivo CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    if file:
        try: 
            with open(file, 'r', newline='') as f:
                csv_file = csv.DictReader(f)
                urls = [row['URL'] for row in csv_file]
                for link in urls:
                    txt_urls.insert(tk.END, link + '\n')
                    projects['hosts'].append(link)
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
    else: 
        tk.messagebox.showerror("Error", f"No se pudo cargar el archivo.")

def run_process():
    asyncio.run(add_txt_raw())

scrap = BeautySoapScrap()

window = tk.Tk()
window.title('UPB APPLICATION')
window.geometry("400x300")
window.configure(bg="lightblue")

btn_upload_csv = tk.Button(window, text="Cargar CSV", command=get_urls_csv)
btn_upload_csv.pack()

lab_urls = tk.Label(window, text='URL\'s Obtenidas del archivo CSV: ')
lab_urls.pack(pady=10)

txt_urls = tk.Text(window)
txt_urls.pack(pady=10)

btn_add_hosts = tk.Button(window, text="Obtener información.", command=run_process)
btn_add_hosts.pack()

lab_get_txt = tk.Label(window, text='')
lab_get_txt.pack(pady=10)

window.mainloop()

# txt = 'Yo te quiero como el mar quiere al río, como la noche quiere al día, como el sol a la luna, como la luz al día.'
# txt_eng = 'I love you like the sea loves the river, like the night loves the day, like the sun loves the moon, like light loves the day.'
# connector = AIOpenAPI()
# response = connector.prompt('Analiza el siguiente texto', txt_eng, 500)
# tx = response.choices[0].text.strip()
# print(tx)