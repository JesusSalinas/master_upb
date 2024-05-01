import tkinter as tk
import json
import csv
import asyncio
import copy

from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.beauty import BeautySoapScrap
from src.interfaces import resources, projects, outcomes
from tkinter import filedialog
from PIL import Image, ImageTk

scrap = BeautySoapScrap()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("UPB APPLICATION")
        self.geometry("1000x700")

        self.welcome_frame = WelcomeFrame(self)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

class WelcomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")

        self.label = tk.Label(self, text="¡BIENVENID@S!", font=("Helvetica", 24), bg="lightblue", fg="black")
        self.label.pack(pady=20)

        self.image = Image.open("./img/background.jpeg") 
        self.image = self.image.resize((300, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image=self.photo, bg="white")
        self.image_label.pack(pady=20)

        self.button = tk.Button(self, text="Iniciar proyecto", font=("Helvetica", 20), bg="gray", fg="black", command=self.start_project)
        self.button.pack(pady=20)

    def start_project(self):
        self.master.welcome_frame.pack_forget()
        init_frame = InitFrame(self.master)
        init_frame.pack(fill=tk.BOTH, expand=True)

class InitFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")

        self.label = tk.Label(self, text="Cargar los datos fuente:", font=("Helvetica", 24), bg="white", fg="black")
        self.label.pack(pady=15)

        self.btn_upload_csv = tk.Button(self, text="Cargar CSV", font=("Helvetica", 14), bg="gray", fg="black", command=self.get_urls_csv)
        self.btn_upload_csv.pack(pady=10)

        self.txt_urls = tk.Text(self)
        self.txt_urls.pack(pady=10)

        self.btn_add_hosts = tk.Button(self, text="Obtener información.", font=("Helvetica", 14), bg="gray", fg="black", command=self.run_process)
        self.btn_add_hosts.pack(pady=10)

        self.lab_get_txt = tk.Label(self, text='')
        self.lab_get_txt.pack(pady=10)

    def get_urls_csv(self):
        urls= []
        file = filedialog.askopenfilename(initialdir="/", title="Selecciona un archivo CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
        if file:
            try: 
                with open(file, 'r', newline='') as f:
                    csv_file = csv.DictReader(f)
                    urls = [row['URL'] for row in csv_file]
                    for link in urls:
                        self.txt_urls.insert(tk.END, link + '\n')
                        projects['hosts'].append(link)
            except Exception as e:
                tk.messagebox.showwarning(message=f"No se pudo cargar el archivo: {e}", title="UPB APPLICATION")
        else: 
            tk.messagebox.showwarning(message="No se pudo cargar el archivo.", title="UPB APPLICATION")
    
    def run_process(self):
        asyncio.run(self.add_txt_raw())

    async def add_txt_raw(self):
        urls = projects['hosts']
        for link in urls:
            host = await scrap.valid_host(link)
            if host:
                resources['txt_raw'].append(copy.deepcopy(scrap.body))
            else: 
                self.txt_urls.insert(tk.END, 'Por favor validar la información del archivo. Error: ' + scrap.err + '\n')
                print(scrap.err)
        if resources['txt_raw']:
            connector = MongoDBConnector()
            connector.connect()
            connector.get_collection('CollectionTest')
            if (connector.collection!=None):
                connector.insert_document(resources)
                #self.lab_get_txt.config(text='Información obtenida correctamente.')
                tk.messagebox.showinfo(message="Información obtenida correctamente.", title="UPB APPLICATION")
        else: 
            tk.messagebox.showwarning(message="Error al obtener la información. Por favor valida que las URL\'s se agregaron correctamente.", title="UPB APPLICATION")

