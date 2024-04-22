import json
import tkinter as tk

from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.scrap import ParseHubScrap
from src.beauty import BeautySoapScrap
from src.interfaces import resources, projects, outcomes

def add_hosts():
    entries=[]
    entries.append(entry_h1.get())
    entries.append(entry_h2.get())
    # To-do: validar que no sea un caracter vacio que obtiene del input porque no reconoce el vacio 
    if entries:
        for entry in entries:
            host = scrap.valid_host(entry)
            if host:
                txt_urls.insert(tk.END, entry + '\n')
                projects['hosts'].append(entry)
                html = scrap.get_data()
                resources['txt_raw'].append(html)
                print(html['title'])
                #print(html)
            else: 
                txt_urls.insert(tk.END, 'Por favor validar la información ingresada. Error: ' + scrap.err + '\n')
                print(scrap.err)
    else:
        txt_urls.insert(tk.END, 'Por favor ingresa la información requerida. Error:')

def add_txt_raw():
    if resources['txt_raw']:
        connector = MongoDBConnector()
        connector.connect()
        connector.get_collection('CollectionTest')
        if (connector.collection!=None):
            connector.insert_document(resources)
            lab_get_txt.config(text='Información obtenida correctamente.')
    else: 
        lab_get_txt.config(text='Error al obtener la información. Por favor valida que las URL\'s se agregaron correctamente. ')

scrap = BeautySoapScrap()

window = tk.Tk()
window.title('UPB APPLICATION')
window.geometry("400x300")
window.configure(bg="lightblue")

entry_h1 = tk.Entry(window, width=30)
entry_h1.pack(pady=10)

entry_h2 = tk.Entry(window, width=30)
entry_h2.pack(pady=10)

btn_add_hosts = tk.Button(window, text="Agregar URL's", command=add_hosts)
btn_add_hosts.pack()

lab_urls = tk.Label(window, text='URL\'s Validas: ')
lab_urls.pack(pady=10)

txt_urls = tk.Text(window)
txt_urls.pack(pady=10)

btn_add_hosts = tk.Button(window, text="Obtener información.", command=add_txt_raw)
btn_add_hosts.pack()

lab_get_txt = tk.Label(window, text='')
lab_get_txt.pack(pady=10)

window.mainloop()