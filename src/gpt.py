import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

env_model=os.getenv('GPT_MODEL')
env_organization=os.getenv('GPT_ORG')
env_vector=os.getenv('GPT_VECTOR_ID')
env_assistant=os.getenv('GPT_ASSITANT_ID')

class AIOpenAPI:
	def __init__(self):
		self.model=env_model
		self.client= OpenAI(organization=env_organization)
		self.vector_store_id=env_vector
		self.assistant_id=env_assistant

	def prompt(self, prompt,  txt_to_analyze, max_tokens):
		try:
			rsp = self.client.completions.create(
				model=self.model,
				prompt=f'{prompt}: {txt_to_analyze}',
				max_tokens=max_tokens
			)
			print('OPEN_AI API PROMPTED SUCCESSFULL!')
			return rsp
		except Exception as e:
			print('OPEN_AI API PROMPTED FAILED!:', e)

	def create_assitant(self, name, instructions, model):
		try:
			assistant = self.client.beta.assistants.create(
				name=name,
				instructions=instructions,
				model=model,
				tools=[{'type': 'file_search'}],
			)
			if assistant.id != None:
				print('CREATE ASSISTANT SUCCESS!')
				return assistant.id
			else:
				print('CREATE ASSISTANT FAILED!')
				return False
		except Exception as e: 
			print('CREATE ASSISTANT FAILED!:', e)
			return False
    
	def create_vector_store(self, name):
		try:
			vector_store = self.client.beta.vector_stores.create(
				name=name
			)
			if vector_store.id != None:
				print('CREATE VECTOR STORE SUCCESS!')
				return vector_store.id
			else:
				print('CREATE VECTOR STORE FAILED!')
				return False
		except Exception as e: 
			print('CREATE VECTOR STORE FAILED!:', e)
			return False
    
	def fetch_vector_store(self):
		try:
			vector_store_files = self.client.beta.vector_stores.files.list(
				vector_store_id=self.vector_store_id
			) 
			if len(vector_store_files['data']) != 0:
				print('FETCH VECTOR STORE FILES SUCCESS!')
				return vector_store_files['data']
			else:
				print('FETCH VECTOR STORE FILES EMPTY!')
				return False
		except Exception as e:
			print('FETCH VECTOR STORE FILES FAILED!:', e)
			return False
    
	def upload_files_to_vector_store(self, file_streams):
		try:
			file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
				vector_store_id=self.vector_store_id,
				files=file_streams
			)
			if file_batch.status != None:
				print('BATCH FILES UPLOADED SUCCESS!')
				return file_batch.status
			else:
				print('BATCH FILES UPLOADED FAILED!')
				return False
		except Exception as e: 
			print('BATCH FILES UPLOADED FAILED!:', e)
			return False
    
	def link_file_to_vector_store(self, file_id):
		try:
			vector_store_file = self.client.beta.vector_stores.files.create(
				vector_store_id=self.vector_store_id,
				file_id=file_id
			)
			if vector_store_file.id != None:
				print('FILE LINKED SUCCESS!')
				return vector_store_file.id
			else:
				print('FILE LINKED FAILED!')
				return False
		except Exception as e: 
			print('FILE LINKED FAILED!:', e)
			return False
		
	def create_file(self, file_path, purpose):
		try:
			file = self.client.files.create(
				file=open(file_path, 'rb'),
				purpose=purpose
			)
			if file.id != None:
				print('FILE CREATED SUCCESS!')
				return file.id
			else:
				print('FILE CREATED FAILED!')
				return False
		except Exception as e: 
			print('FILE CREATED FAILED!:', e)
			return False
    
	def update_assitant(self):
		try:
			assistant = self.client.beta.assistants.update(
				assistant_id=self.assitant_id,
				tool_resources={'file_search': {'vector_store_ids': [self.vector_store_id]}},
			)
			if assistant.id != None:
				print('ASSISTANT UPDATED SUCCESS!')
				return assistant.id
			else:
				print('ASSISTANT UPDATED FAILED!')
				return False
		except Exception as e: 
			print('ASSISTANT UPDATED FAILED!:', e)
			return False
    
	def create_thread_messages(self, messages):
		try:
			thread = self.client.beta.threads.create(
				messages=[messages]
			)
			if thread.id != None:
				print('THREAD CREATED SUCCESS!')
				return thread.id
			else:
				print('THREAD CREATED FAILED!')
				return False
		except Exception as e: 
			print('THREAD CREATED FAILED!:', e)
			return False
    
	def create_empty_thread(self):
		try:
			thread = self.client.beta.threads.create()
			if thread.id != None:
				print('THREAD CREATED SUCCESS!')
				return thread.id
			else:
				print('THREAD CREATED FAILED!')
				return False
		except Exception as e: 
			print('THREAD CREATED FAILED!:', e)
			return False
    
	def run_poll_thread(self, thread_id):
		try:
			run = self.client.beta.threads.runs.create_and_poll(
				thread_id=thread_id,
				assistant_id=self.assistant_id
			)
			if run.id != None:
				print('RUN THREAD CREATED SUCCESS!')
				return run
			else:
				print('RUN THREAD CREATED FAILED!')
				return False
		except Exception as e: 
			print('RUN THREAD CREATED FAILED!:', e)
			return False
    
	def fetch_thread_messages_list(self, thread_id, run_id):
		try:
			thread_messages = self.client.beta.threads.messages.list(
				thread_id=thread_id,
				run_id=run_id
			)
			for message in thread_messages:
				print(message)
			return False
			# if len(thread_messages['data']) != 0:
			# 	print('FETCH THREAD MESSAGES SUCCESS!')
			# 	return list(thread_messages['data'])
			# else:
			# 	print('FETCH THREAD MESSAGES EMPTY!')
			# 	return False
		except Exception as e: 
			print('FETCH THREAD MESSAGES FAILED!:', e)
			return False
    
	def create_thread_message(self, thread_id, role, content):
		try:
			thread_message = self.client.beta.threads.messages.create(
				thread_id,
				role=role,
				content=content,
			)
			if thread_message.id != None:
				print('MESSAGE THREAD CREATED SUCCESS!')
				return thread_message.id
			else:
				print('MESSAGE THREAD CREATED FAILED!')
				return False
		except Exception as e: 
			print('MESSAGE THREAD CREATED FAILED!:', e)
			return False
    
	def fetch_thread_message(self, thread_id, message_id):
		try:
			message = self.client.beta.threads.messages.retrieve(
				message_id=message_id,
				thread_id=thread_id,
			)
			if message.id != None:
				print('MESSAGE THREAD CREATED SUCCESS!')
				return message.id
			else:
				print('MESSAGE THREAD CREATED FAILED!')
				return False
		except Exception as e: 
			print('MESSAGE THREAD CREATED FAILED!:', e)
			return False