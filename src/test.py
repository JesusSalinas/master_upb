
from interfaces import resources, projects
from gpt import AIOpenAPI

gpt = AIOpenAPI()

file_name = 'txt_to_analyze.txt'
file_path = f'../data/{file_name}'

def create_txt_to_analyze_file(file_path):
    if resources['txt_to_analyze']:
        try:
            with open(file_path, 'w') as file:
                file.write(resources['txt_to_analyze'])
                return True
        except Exception as e:
            print('errorr...')
            return False
    else:
        print('vacio')
        return False

txt = create_txt_to_analyze_file(file_path)

msg = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Usando como apoyo los archivos almacenados en el vector store"
        },
        {
            "type": "text",
            "text": "Describe brevemente Generalidades del Cemento Verde:"
        },
        {
            "type": "text",
            "text": "Describe brevemente Uso o aplicación en Colombia del Cemento Verde"
        },
        {
            "type": "text",
            "text": "Describe brevemente Descripción del Cemento Verde"
        }
    ]
}

if txt :
    file_assistant = gpt.create_file(file_path, 'assistants')
    print(file_assistant)
    vectore_store_file = gpt.link_file_to_vector_store(file_assistant)
    print(vectore_store_file)
    thread = gpt.create_thread_messages(msg)
    print(thread)
    run = gpt.run_poll_thread(thread)
    if(run.status == 'completed'):
        msgs = gpt.fetch_thread_messages_list(thread, run.id)
        if msgs != False:
            print(msgs)
    elif (run.status == 'expired' or run.status == 'failed' or run.status == 'incomplete' or run.status == 'cancelled'):
        print('error')

else:
    print('error')