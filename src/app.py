import tkinter as tk
import json
import csv
import asyncio
import copy
import threading
import time
import re

from tkinter import ttk
from src.mongo import MongoDBConnector
from src.gpt import AIOpenAPI
from src.beauty import BeautySoapScrap
from data.objs import resources, projects, assistant_thread_messages
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import date
from bson import ObjectId

scrap = BeautySoapScrap()
gpt = AIOpenAPI()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('UPB APPLICATION')
        self.geometry('1000x700')

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

        self.configure(bg='white')
        self.label_title = tk.Label(self, text='¡BIENVENID@S!', font=('Helvetica', 24), bg='lightblue', fg='black')
        self.label_title.pack(pady=20)

        self.image = Image.open('./img/background.jpeg') 
        self.image = self.image.resize((300, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self, image=self.photo, bg='white')
        self.image_label.pack(pady=20)

        self.btn_new_project = tk.Button(self, text='Nuevo proyecto', font=('Helvetica', 20), bg='gray', fg='black', command=self.start_project)
        self.btn_new_project.pack(side=tk.LEFT, padx=100, pady=10)

        self.btn_select_project = tk.Button(self, text='Elegir proyecto', font=('Helvetica', 20), bg='gray', fg='black', command=self.select_project)
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
            self.btn_select = tk.Button(self, text='Continuar', font=('Helvetica', 20), bg='gray', fg='black', command=self.continue_project)
            self.btn_select.pack(pady=10)
        else:
            tk.messagebox.showwarning(message='No hay projectos iniciados.', title='UPB APPLICATION') 

    def continue_project(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            print('Elemento seleccionado:', selected_item)
        else:
            tk.messagebox.showwarning(message='No hay projecto seleccionado.', title='UPB APPLICATION') 

class InitFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white')
        self.label_title = tk.Label(self, text='Paso #1: Creación del proyecto', font=('Helvetica', 24), bg='white', fg='black')
        self.label_title.pack(pady=5)

        self.label_name = tk.Label(self, text='Nombre del proyecto:', font=('Helvetica', 20), bg='white', fg='black')
        self.label_name.pack(pady=5)

        self.text_name = tk.Entry(self)
        self.text_name.pack(pady=5, padx=200, fill=tk.X)

        self.label_author = tk.Label(self, text='Autor del proyecto:', font=('Helvetica', 20), bg='white', fg='black')
        self.label_author.pack(pady=5)

        self.text_author = tk.Entry(self)
        self.text_author.pack(pady=5, padx=200, fill=tk.X)

        self.label_topic = tk.Label(self, text='Tema del proyecto:', font=('Helvetica', 20), bg='white', fg='black')
        self.label_topic.pack(pady=5)

        self.text_topic = tk.Entry(self)
        self.text_topic.pack(pady=5, padx=200, fill=tk.X)

        self.label_desc = tk.Label(self, text='Descripción del proyecto:', font=('Helvetica', 20), bg='white', fg='black')
        self.label_desc.pack(pady=5)

        self.text_desc = tk.Entry(self)
        self.text_desc.pack(pady=5, padx=60, fill=tk.X)

        self.btn_save_info = tk.Button(self, text='Guardar', font=('Helvetica', 20), bg='gray', fg='black', command=self.save_info_project)
        self.btn_save_info.pack(pady=5)

    def save_info_project(self):
        project_name = self.text_name.get()
        author = self.text_author.get()
        topic = self.text_topic.get()
        description = self.text_desc.get()
        project_date = str(date.today())
        if(project_name == '' or author == '' or description == '' or topic == ''):
            tk.messagebox.showwarning(message='Valida que los campos no sean vacíos', title='UPB APPLICATION')
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
               tk.messagebox.showwarning(message='Valida la información ingresada. Hubo un error al guardar el proyecto.', title='UPB APPLICATION') 

class ScrapFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white')

        self.label_project = tk.Label(self, text=f'Proyecto: {projects["project_name"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_project.pack(side='top', anchor='nw')
        
        self.label_topic = tk.Label(self, text=f'Tema: {projects["topic"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_topic.pack(side='top', anchor='ne', pady=0)

        self.label_title = tk.Label(self, text='Paso #2: Proceso web scrapping', font=('Helvetica', 24), bg='white', fg='black')
        self.label_title.pack(pady=5)
        
        self.label_upload_file = tk.Label(self, text='Cargar los datos fuente:', font=('Helvetica', 24), bg='white', fg='black')   
        self.label_upload_file.pack(pady=5)
        
        self.btn_upload_csv = tk.Button(self, text='Cargar CSV', font=('Helvetica', 24), bg='gray', fg='black', command=self.get_urls_csv)
        self.btn_upload_csv.pack(pady=5)

        self.txt_urls = tk.Text(self)
        self.txt_urls.pack(pady=5)

        self.btn_add_hosts = tk.Button(self, text='Obtener información', font=('Helvetica', 24), bg='gray', fg='black', command=self.run_process)
        self.btn_add_hosts.pack(pady=5)

    def get_urls_csv(self):
        urls= []
        file = filedialog.askopenfilename(initialdir='/', title='Selecciona un archivo CSV', filetypes=(('Archivos CSV', '*.csv'), ('Todos los archivos', '*.*')))
        if file:
            try: 
                with open(file, 'r', newline='') as f:
                    csv_file = csv.DictReader(f)
                    urls = [row['URL'] for row in csv_file]
                    for link in urls:
                        self.txt_urls.insert(tk.END, link + '\n')
                        projects['research_source'].append(link)
            except Exception as e:
                tk.messagebox.showwarning(message=f'No se pudo cargar el archivo: {e}', title='UPB APPLICATION')
        else: 
            tk.messagebox.showwarning(message='No se pudo cargar el archivo.', title='UPB APPLICATION')
    
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
            doc = connector.insert_document(resources, 'Resources')
            connector.disconnect()
            if doc != False:
                #To-Do update el status del projecto
                projects['status'] = 'SCRAPED_DATA'
                tk.messagebox.showinfo(message='Información obtenida correctamente.', title='UPB APPLICATION')
                self.master.drop_scrap()
                self.master.add_data_clean()
            else:
                tk.messagebox.showwarning(message='Error al guardar la información. Por favor valida que el archivo CSV fue cargado correctamente.', title='UPB APPLICATION')
        else: 
            tk.messagebox.showwarning(message='Error al obtener la información. Por favor valida que el archivo CSV fue cargado correctamente.', title='UPB APPLICATION')

class DataCleanFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg='white')

        self.label_project = tk.Label(self, text=f'Proyecto: {projects["project_name"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_project.pack(side='top', anchor='nw')
        
        self.label_topic = tk.Label(self, text=f'Tema: {projects["topic"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_topic.pack(side='top', anchor='ne')

        self.label_title = tk.Label(self, text='Paso #3: Proceso de limpieza de texto', font=('Helvetica', 24), bg='white', fg='black')
        self.label_title.pack(pady=5)

        self.label_description = tk.Label(self, text='Aquí podras realizar la limipeza/preparación de la información extraída en el paso atnerior o elegir que la aplicación lo realize.\n Por favor da click en Continuar', font=('Helvetica', 14), bg='white', fg='black')
        self.label_description.pack(pady=5)

        self.button_question = tk.Button(self, text='Continuar', font=('Helvetica', 20), bg='gray', fg='black', command=self.show_choice_message)
        self.button_question.pack(pady=5)

    def show_choice_message(self):
        result = tk.messagebox.askquestion('Selección de Acción', '¿Deseas realizar manualmente la limpieza de Texto?',
                                        icon='question', 
                                        type='yesnocancel')
        
        if result == 'yes':
            self.button_question.pack_forget()
            self.label_description.configure(text='Realiza la descarga del Texto obtenido por Web Scraping. Limpia la información y sube un documento nuevo.')
            self.button_download = tk.Button(self, text='Descargar Archivo', font=('Helvetica', 20), bg='gray', fg='black', command=self.download_file)
            self.button_download.pack(pady=5)
        elif result == 'no':
            self.clean_txt()
        else:
            print('USER CANCEL CLEAN DATA')

    def upload_txt_clean(self):
        file = filedialog.askopenfilename(initialdir='/', title='Selecciona un archivo TXT', filetypes=(('Archivos de texto', '*.txt'), ('Todos los archivos', '*.*')))
        if file:
            try: 
                with open(file, 'r', newline='') as f:
                    content = f.read()
                    resources['txt_to_analyze'] = content
                    # To-do validar linea anterior
                    if content:
                        self.master.drop_data_clean()
                        self.master.add_txt_analysis()
                    else:
                        tk.messagebox.showwarning(message=f'Archivo vacio. Por favor valida la información cargada.', title='UPB APPLICATION')
            except Exception as e:
                tk.messagebox.showwarning(message=f'No se pudo cargar el archivo: {e}', title='UPB APPLICATION')
        else: 
            tk.messagebox.showwarning(message='No se pudo cargar el archivo.', title='UPB APPLICATION')

    def download_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Archivos de texto', '*.txt')])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write('Este es un archivo de texto generado automáticamente.')
                    #To-do implementar la generación del archivo a partir del json resourcers
                tk.messagebox.showwarning(message='El archivo se ha descargado correctamente.', title='UPB APPLICATION')
                self.button_download.pack_forget()
                self.btn_upload_file = tk.Button(self, text='Cargar archivo', font=('Helvetica', 20), bg='gray', fg='black', command=self.upload_txt_clean)
                self.btn_upload_file.pack(pady=5)

            except Exception as e:
                tk.messagebox.showwarning(message=f'Error al descargar el archivo. Intenta nuevamente.{e}', title='UPB APPLICATION')

    def clean_txt(self):
        print('Limpiando datos...')
        all_txt = ""
        for obj in resources['txt_raw']:
            if 'title' in obj and obj['title']:
                all_txt += ' ' + obj['title']
            
            if 'bullets' in obj and isinstance(obj['bullets'], list):
                for bullet in obj['bullets']:
                    if bullet:
                        all_txt += ' ' + bullet

            if 'paragraphs' in obj and isinstance(obj['paragraphs'], list):
                for paragraph in obj['paragraphs']:
                    if paragraph:
                        all_txt += ' ' + paragraph
        
        all_txt = all_txt.lower()
        all_txt = re.sub(r'[^a-zA-Z0-9\s]', '', all_txt)
        all_txt = re.sub(r'\s+', ' ', all_txt).strip()

        resources['txt_to_analyze'] = all_txt
        #To-Do agregarlo a la DB

        self.master.drop_data_clean()
        self.master.add_txt_analysis()

class TxtAnalysisFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.file_name = 'txt_to_analyze.txt'
        self.file_path = f'./docs/{self.file_name}'

        self.configure(bg='white')

        self.label_project = tk.Label(self, text=f'Proyecto: {projects["project_name"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_project.pack(side='top', anchor='nw')
        
        self.label_topic = tk.Label(self, text=f'Tema: {projects["topic"]}', font=('Helvetica', 14), bg='lightblue', fg='black')
        self.label_topic.pack(side='top', anchor='ne')

        self.label_title = tk.Label(self, text='Paso #4: Proceso de Analysis de Texto', font=('Helvetica', 24), bg='white', fg='black')
        self.label_title.pack(pady=5)

        self.label_description = tk.Label(self, text='Aquí podras realizar el analysis de la información. \n Por favor elige los puntos que deseas obtener del tema del projecto.', font=('Helvetica', 14), bg='white', fg='black')
        self.label_description.pack(pady=5)

        style = ttk.Style(self)
        style.configure('Custom.Horizontal.TProgressbar', troughcolor='white', background='green', thickness=50) 
        self.progress_bar = ttk.Progressbar(self, style="Custom.Horizontal.TProgressbar", orient=tk.HORIZONTAL, length=500, mode='indeterminate')

        self.checkboxes = []
        connector = MongoDBConnector()
        connector.connect()
        query = { 'prompts': 'Generalidades' }
        document = connector.find_document('Catalogs', query)
        connector.disconnect()
        if document != False:
            doc = json.loads(document)
            for catalogue in doc['prompts']:
                checkbox_var = tk.BooleanVar()
                checkbox = tk.Checkbutton(self, text=catalogue, variable=checkbox_var, bg='gray')
                checkbox.pack(anchor='center', pady=5)
                self.checkboxes.append((checkbox_var, catalogue))
        else: 
            print('FETCH CATALOGUES FAILED!')

        self.btn_txt_analysis = tk.Button(self, text='Analizar Información.', font=('Helvetica', 20), bg='gray', fg='black', command=self.txt_analysis)
        self.btn_txt_analysis.pack(pady=15)

    def txt_analysis(self):
        checked_values = []
        if self.file_path:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(resources['txt_to_analyze'])
            except Exception as e:
                tk.messagebox.showwarning(message=f'Error al guardar el texto analizar: {e}', title='UPB APPLICATION')

        for checkbox_var, catalogue in self.checkboxes:
            if checkbox_var.get():
                checked_values.append(catalogue)
        
        txt = self.create_txt_to_analyze_file()

        if checked_values:
            assistant_thread_messages['role'] = 'user'
            for value in checked_values:
                prompt = {
                    'type': 'text',
                    'text': f'Describe detalladamente: {value} del {projects["topic"]}'
                }
                assistant_thread_messages['content'].append(prompt)
            if txt:
                self.start_thread(assistant_thread_messages)
            else:
                print('File no created. This is only informative.')
        else:
            tk.messagebox.showwarning(message='Debes elegir al menos una opción.', title='UPB APPLICATION')

    def create_txt_to_analyze_file(self):
        if resources['txt_to_analyze']:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(resources['txt_to_analyze'])
                    print('FILE CREATED LOCAL SUCCESSFULL!')
                    return True
            except Exception as e:
                tk.messagebox.showwarning(message=f'Error al crear el achivo analizar: {e}', title='UPB APPLICATION')
                return False
        else:
            tk.messagebox.showwarning(message='No se encontro texto para analizar. Favor de reviar el proceso. ', title='UPB APPLICATION')
            return False

    def start_thread(self, msg):
        self.btn_txt_analysis.config(state='disabled')
        self.progress_bar.pack(pady=20, fill=None, anchor='center')
        self.progress_bar.start()
        time.sleep(20)
        #threading.Thread(target=self.gpt_analyis(msg)).start()

    def gpt_analyis(self, msg):
        txt_resources = projects['research_source']
        txt_outcome = ''
        document_id = resources['project_id']
        mongo_filter = {'_id': ObjectId(document_id)}
        file_assistant = gpt.create_file(self.file_path, 'assistants')
        vectore_store_file = gpt.link_file_to_vector_store(file_assistant)
        if vectore_store_file:
            thread = gpt.create_thread_messages(msg)
            run = gpt.run_poll_thread(thread)
            if(run.status == 'completed'):
                msgs = gpt.fetch_thread_messages_list(thread, run.id)
                if msgs != False:
                    for msg in msgs:
                        txt_outcome = msg.content[0].text.value
                        #print(txt_outcome)
            elif (run.status == 'expired' or run.status == 'failed' or run.status == 'incomplete' or run.status == 'cancelled'):
                tk.messagebox.showwarning(message='El proceso de Analisis tuvo un error.', title='UPB APPLICATION')
            obj_outcome = {'outcomes': txt_outcome, 'research_source': txt_resources}
            connector = MongoDBConnector()
            connector.connect()
            doc = connector.update_document(mongo_filter, 'Projects', obj_outcome)
            connector.disconnect()
            self.progress_bar.stop()
            self.btn_txt_analysis.config(state='normal')
            if doc:
                tk.messagebox.showinfo(message='Analisis de Datos Finalizo Correctamente.', title='UPB APPLICATION')
        else:
            tk.messagebox.showwarning(message='El proceso de Analisis tuvo un error al asociar el archivo a procesar.', title='UPB APPLICATION')