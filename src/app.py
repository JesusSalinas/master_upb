import tkinter as tk
import json
import csv
import asyncio
import copy

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

    def add_init(self):
        self.init_frame = InitFrame(self)
        self.init_frame.pack(fill=tk.BOTH, expand=True)
    def add_txt_analysis(self):
        self.txt_analysis_frame = TxtAnalysisFrame(self)
        self.txt_analysis_frame.pack(fill=tk.BOTH, expand=True)
    def add_scrap(self):
        self.scrap_frame = ScrapFrame(self)
        self.scrap_frame.pack(fill=tk.BOTH, expand=True)
    def add_data_clean(self):
        self.data_clean_frame = DataCleanFrame(self)
        self.data_clean_frame.pack(fill=tk.BOTH, expand=True)
    def drop_init(self):
        self.init_frame.pack_forget()
    def drop_welcome(self):
        self.welcome_frame.pack_forget()
    def drop_scrap(self):
        self.scrap_frame.pack_forget()
    def drop_data_clean(self):
        self.data_clean_frame.pack_forget()
    def drop_txt_analysi(self):
        self.txt_analysis_frame.pack_forget()

class WelcomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")
        self.label_title = tk.Label(self, text="¡BIENVENID@S!", font=("Helvetica", 24), bg="lightblue", fg="black")
        self.label_title.pack(pady=20)

        self.image = Image.open("./img/background.jpeg") 
        self.image = self.image.resize((300, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image=self.photo, bg="white")
        self.image_label.pack(pady=20)

        self.btn_new_project = tk.Button(self, text="Iniciar nuevo proyecto", font=("Helvetica", 20), bg="gray", fg="black", command=self.start_project)
        self.btn_new_project.pack(side=tk.LEFT, padx=100, pady=10)

        self.btn_select_project = tk.Button(self, text="Elegir proyecto", font=("Helvetica", 20), bg="gray", fg="black", command=self.select_project)
        self.btn_select_project.pack(side=tk.RIGHT, padx=100, pady=10)

    def start_project(self):
        self.master.drop_welcome()
        self.master.add_init()

    def select_project(self):
        connector = MongoDBConnector()
        connector.connect()
        documents = connector.fetch_documents('Projects')
        connector.disconnect()
        if documents != False:
            docs = [json.loads(doc) for doc in documents]
            self.btn_new_project.pack_forget()
            self.btn_select_project.pack_forget()
            self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
            self.listbox.pack(pady=10, padx=100, fill=tk.BOTH, expand=True)
            #self.listbox.config(yscrollcommand=self.listbox.scrollbar.set)
            #self.scrollbar = tk.Scrollbar(self.listbox, orient=tk.VERTICAL, command=self.listbox.yview)
            #self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            for doc in docs:
                self.listbox.insert(tk.END, doc['project_name'])
            self.btn_select = tk.Button(self, text="Continuar", font=("Helvetica", 20), bg="gray", fg="black", command=self.continue_project)
            self.btn_select.pack(pady=10)
        else:
            tk.messagebox.showwarning(message="No hay projectos iniciados.", title="UPB APPLICATION") 

    def continue_project(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            print("Elemento seleccionado:", selected_item)
        else:
            tk.messagebox.showwarning(message="No hay projecto seleccionado.", title="UPB APPLICATION") 

class InitFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")
        self.label_title = tk.Label(self, text="Paso #1: Creación del proyecto", font=("Helvetica", 24), bg="white", fg="black")
        self.label_title.pack(pady=5)

        self.label_name = tk.Label(self, text="Nombre del proyecto:", font=("Helvetica", 20), bg="white", fg="black")
        self.label_name.pack(pady=5)

        self.text_name = tk.Entry(self)
        self.text_name.pack(pady=5, padx=200, fill=tk.X)

        self.label_author = tk.Label(self, text="Autor del proyecto:", font=("Helvetica", 20), bg="white", fg="black")
        self.label_author.pack(pady=5)

        self.text_author = tk.Entry(self)
        self.text_author.pack(pady=5, padx=200, fill=tk.X)

        self.label_topic = tk.Label(self, text="Tema del proyecto:", font=("Helvetica", 20), bg="white", fg="black")
        self.label_topic.pack(pady=5)

        self.text_topic = tk.Entry(self)
        self.text_topic.pack(pady=5, padx=200, fill=tk.X)

        self.label_desc = tk.Label(self, text="Descripción del proyecto:", font=("Helvetica", 20), bg="white", fg="black")
        self.label_desc.pack(pady=5)

        self.text_desc = tk.Entry(self)
        self.text_desc.pack(pady=5, padx=60, fill=tk.X)

        self.btn_save_info = tk.Button(self, text="Guardar", font=("Helvetica", 20), bg="gray", fg="black", command=self.save_info_project)
        self.btn_save_info.pack(pady=5)

    def save_info_project(self):
        project_name = self.text_name.get()
        author = self.text_author.get()
        topic = self.text_topic.get()
        description = self.text_desc.get()
        project_date = str(date.today())
        if(project_name == '' or author == '' or description == '' or topic == ''):
            tk.messagebox.showwarning(message="Valida que los campos no sean vacíos", title="UPB APPLICATION")
        else:
            projects['project_name'] = project_name
            projects['description'] = description
            projects['topic'] = topic
            projects['started_date'] = project_date
            projects['author'] = author
            projects['status'] = 'INITIATED'

            connector = MongoDBConnector()
            connector.connect()
            doc = connector.insert_document(projects, 'Projects')
            connector.disconnect()
            if doc != False:
                projects['project_id'] = doc
                self.master.drop_init()
                self.master.add_scrap()
            else:
               tk.messagebox.showwarning(message="Valida la información ingresada. Hubo un error al guardar el proyecto.", title="UPB APPLICATION") 

class ScrapFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")
        self.label_title = tk.Label(self, text="Paso #2: Proceso web scrapping", font=("Helvetica", 24), bg="white", fg="black")
        self.label_title.pack(pady=5)
        
        self.label_project = tk.Label(self, text=f"Proyecto: {projects['project_name']}", font=("Helvetica", 14), bg="lightblue", fg="black")
        self.label_project.pack(side=tk.LEFT)
        #self.label_project.place(y=0)
        
        self.label_topic = tk.Label(self, text=f"Tema: {projects['topic']}", font=("Helvetica", 14), bg="lightblue", fg="black")
        self.label_topic.pack(side=tk.RIGHT)
        #self.label_topic.place(y=10, x=-1)
        
        self.label_upload_file = tk.Label(self, text="Cargar los datos fuente:", font=("Helvetica", 24), bg="white", fg="black")   
        self.label_upload_file.pack(pady=5)
        
        self.btn_upload_csv = tk.Button(self, text="Cargar CSV", font=("Helvetica", 24), bg="gray", fg="black", command=self.get_urls_csv)
        self.btn_upload_csv.pack(pady=5)

        self.txt_urls = tk.Text(self)
        self.txt_urls.pack(pady=5)

        self.btn_add_hosts = tk.Button(self, text="Obtener información", font=("Helvetica", 24), bg="gray", fg="black", command=self.run_process)
        self.btn_add_hosts.pack(pady=5)

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

    async def add_txt_raw(self):
        urls = projects['research_source']
        resource_date = str(date.today())
        resources['date'] = resource_date
        resources['project_id'] = projects['project_id']
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
            doc = connector.insert_document(resources, 'CollectionTest')
            connector.disconnect()
            if doc != False:
                #To-Do update el status del projecto
                tk.messagebox.showinfo(message="Información obtenida correctamente.", title="UPB APPLICATION")
                self.master.drop_scrap()
                self.master.add_data_clean()
            else:
                tk.messagebox.showwarning(message="Error al guardar la información. Por favor valida que el archivo CSV fue cargado correctamente.", title="UPB APPLICATION")
        else: 
            tk.messagebox.showwarning(message="Error al obtener la información. Por favor valida que el archivo CSV fue cargado correctamente.", title="UPB APPLICATION")

class DataCleanFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")

class TxtAnalysisFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="white")

        # self.checkboxes = []
        # connector = MongoDBConnector()
        # connector.connect()
        # query = { "prompts": "Generalidades" }
        # document = connector.find_document('Catalogs', query)
        # connector.disconnect()
        # if document != False:
        #     doc = json.loads(document)
        #     for catalogue in doc['prompts']:
        #         checkbox_var = tk.BooleanVar()
        #         checkbox = tk.Checkbutton(self, text=catalogue, variable=checkbox_var, bg="gray")
        #         checkbox.pack(anchor=tk.W)
        #         self.checkboxes.append(checkbox_var)
        # else: 
        #     print('ERROR Catalogues')