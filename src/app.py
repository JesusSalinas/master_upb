import tkinter as tk
import json
import csv
import asyncio
import copy
import uuid

from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.beauty import BeautySoapScrap
from src.interfaces import resources, projects
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import date

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

        self.button = tk.Button(self, text="Iniciar nuevo proyecto", font=("Helvetica", 20), bg="gray", fg="black", command=self.start_project)
        self.button.pack(pady=20)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.listbox.insert(tk.END, "Elemento 1")
        self.listbox.insert(tk.END, "Elemento 2")
        self.listbox.insert(tk.END, "Elemento 3")
        self.listbox.insert(tk.END, "Elemento 4")

    def start_project(self):
        self.master.welcome_frame.pack_forget()
        init_frame = InitFrame(self.master)
        init_frame.pack(fill=tk.BOTH, expand=True)

class InitFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")

        # self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.label_name = tk.Label(self, text="Nombre del proyecto:", font=("Helvetica", 24), bg="white", fg="black")
        self.label_name.pack(pady=5)

        self.text_name = tk.Entry(self)
        self.text_name.pack(pady=5, padx=200, fill=tk.X)

        self.label_author = tk.Label(self, text="Autor del proyecto:", font=("Helvetica", 24), bg="white", fg="black")
        self.label_author.pack(pady=5)

        self.text_author = tk.Entry(self)
        self.text_author.pack(pady=5, padx=200, fill=tk.X)

        self.label_desc = tk.Label(self, text="Descripción del proyecto:", font=("Helvetica", 24), bg="white", fg="black")
        self.label_desc.pack(pady=5)

        self.text_desc = tk.Entry(self)
        self.text_desc.pack(pady=5, padx=60, fill=tk.X)

        self.btn_save_info = tk.Button(self, text="Guardar", font=("Helvetica", 24), bg="gray", fg="black", command=self.save_info_project)
        self.btn_save_info.pack(pady=5)

        self.label_upload_file = tk.Label(self, text="Cargar los datos fuente:", font=("Helvetica", 24), bg="white", fg="black")    
        self.btn_upload_csv = tk.Button(self, text="Cargar CSV", font=("Helvetica", 24), bg="gray", fg="black", command=self.get_urls_csv)
        self.txt_urls = tk.Text(self)
        self.btn_add_hosts = tk.Button(self, text="Obtener información", font=("Helvetica", 24), bg="gray", fg="black", command=self.run_process)
        

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
                        projects['research_source'].append(link)
            except Exception as e:
                tk.messagebox.showwarning(message=f"No se pudo cargar el archivo: {e}", title="UPB APPLICATION")
        else: 
            tk.messagebox.showwarning(message="No se pudo cargar el archivo.", title="UPB APPLICATION")
    
    def run_process(self):
        asyncio.run(self.add_txt_raw())

    def save_info_project(self):
        project_name = self.text_name.get()
        author = self.text_author.get()
        description = self.text_desc.get()
        project_id = uuid.uuid4()
        project_date = date.today()
        if(project_name == '' or author == '' or description == ''):
            tk.messagebox.showwarning(message="Valida que los campos no sean vacíos", title="UPB APPLICATION")
        else:
            projects['project_id'] = project_id
            projects['project_name'] = project_name
            projects['description'] = description
            projects['started_date'] = project_date
            projects['author'] = author
            projects['status'] = 'INITIATED'
            connector = MongoDBConnector()
            connector.connect()
            connector.insert_document(projects, 'Projects')
            # TO-DO validar que se inserto bien el documento esta fallando por el uuid
            connector.disconnect()
            self.label_name.pack_forget()
            self.text_name.pack_forget()
            self.label_author.pack_forget()
            self.text_author.pack_forget()
            self.label_desc.pack_forget()
            self.text_desc.pack_forget()
            self.btn_save_info.pack_forget()
            self.label_project = tk.Label(self, text=f"Proyecto: {project_name}", font=("Helvetica", 14), bg="lightblue", fg="black")
            self.label_project.pack(pady=0)
            self.label_project.place(x=0, y=0)
            self.label_upload_file.pack(pady=5)
            self.btn_upload_csv.pack(pady=5)
            self.txt_urls.pack(pady=5)
            self.btn_add_hosts.pack(pady=5)

    async def add_txt_raw(self):
        urls = projects['research_source']
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
            connector.insert_document(resources, 'CollectionTest')
            tk.messagebox.showinfo(message="Información obtenida correctamente.", title="UPB APPLICATION")
            connector.disconnect()
            #connector.get_collection('CollectionTest')
            # if (connector.collection!=None):
            #     connector.insert_document(resources)
            #     tk.messagebox.showinfo(message="Información obtenida correctamente.", title="UPB APPLICATION")
        else: 
            tk.messagebox.showwarning(message="Error al obtener la información. Por favor valida que el archivo CSV fue cargado correctamente.", title="UPB APPLICATION")

