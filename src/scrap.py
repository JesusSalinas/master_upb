import os
import requests

from dotenv import load_dotenv
load_dotenv()

env_api_key = os.getenv('HUB_API_KEY')
env_host = os.getenv('HUB_HOST')
env_project_token = os.getenv('HUB_PROJECT_TOKEN')

params = {
  "api_key": env_api_key,
  "format": "json"
}

class ParseHubScrap:

	""" This Class """

	def __init__(self):
		self.host=env_host
		self.project= None

	def get_project(self, project):
		""" This Function """
		base_url = self.host + '/projects/' + project
		try:
			get_data = requests.get(base_url, params=params)
			if get_data.status_code == 200:
				print("FETCH PROJECT INFO SUCCESSFULL!")
				return get_data.text
			else:
				print("FETCH PROJECT INFO FAILED!")
		except Exception as e:
			print("FETCH PROJECT INFO FAILED!:", e)

	def get_all_projects(self):
		""" This Function """
		base_url = self.host + '/projects'
		try:
			get_data = requests.get(base_url, params=params)
			if get_data.status_code == 200:
				print("FETCH ALL PROJECTS SUCCESSFULL!")
				return get_data.text
			else:
				print("FETCH ALL PROJECTS FAILED!")
		except Exception as e:
			print("FETCH ALL PROJECTS FAILED!:", e)

	def run_project(self, project):
		""" This Function """
		base_url = self.host + '/projects/' + project + '/run'
		try:
			get_data = requests.post(base_url, params=params)
			if get_data.status_code == 200:
				print("RUN PROJECT SUCCESSFULL!")
				return get_data.text
			else:
				print("RUN PROJECT FAILED!")
		except Exception as e:
			print("RUN PROJECT FAILED!:", e)

	def run_status(self, run_token):
		""" This Function """
		base_url = self.host + '/runs/' + run_token
		try:
			get_data = requests.get(base_url, params=params)
			if get_data.status_code == 200:
				print("FETCH STATUS PROJECT SUCCESSFULL!")
				return get_data.text
			else:
				print("FETCH STATUS PROJECT FAILED!")
		except Exception as e:
			print("FETCH STATUS PROJECT FAILED!:", e)

	def get_data_run(self, run_token):
		""" This Function """
		base_url = self.host + '/runs/' + run_token + '/data'
		try:
			get_data = requests.get(base_url, params=params)
			if get_data.status_code == 200:
				print("FETCH DATA RUN SUCCESSFULL!")
				return get_data.text
			else:
				print("FETCH DATA RUN FAILED!")
		except Exception as e:
			print("FETCH DATA RUN FAILED!:", e)
