import requests
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
  def __init__(self):
    self.host=env_host
    self.project= None

  def get_project(self, project):
    base_url = self.host + '/projects/' + project
    try:
      getData = requests.get(base_url, params=params)
      print("FETCH PROJECT INFO SUCCESSFULL!")
      return getData.text
    except Exception as e:
      print("FETCH PROJECT INFO FAILED!:", e)
    
  def run_project(self, project):
    base_url = self.host + '/projects/' + project + '/run'
    try:
      getData = requests.post(base_url, params=params)
      print("RUN PROJECT SUCCESSFULL!")
      return getData.text
    except Exception as e:
      print("RUN PROJECT FAILED!:", e)

  def run_status(self, run_token):
    base_url = self.host + '/runs/' + run_token
    try:
      getData = requests.get(base_url, params=params)
      print("FETCH STATUS PROJECT SUCCESSFULL!")
      return getData.text
    except Exception as e:
      print("FETCH STATUS PROJECT FAILED!:", e)

  def get_data_run(self, run_token):
    base_url = self.host + '/runs/' + run_token + '/data'
    try:
      getData = requests.get(base_url, params=params)
      print("FETCH DATA RUN SUCCESSFULL!")
      return getData.text
    except Exception as e:
      print("FETCH DATA RUN FAILED!:", e)