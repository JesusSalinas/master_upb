import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

env_model=os.getenv('GPT_MODEL')
env_organization=os.getenv('GPT_ORG')

class AIOpenAPI:
  def __init__(self):
    self.model=env_model
    self.client= OpenAI(organization=env_organization)

  def prompt(self, txt_to_analyze, max_tokens):
    try:
      rsp = self.client.completions.create(
        model=self.model,
        prompt=f"Analiza el siguiente texto: {txt_to_analyze}",
        max_tokens=max_tokens
      )
      print('OPEN_AI API PROMPTED SUCCESSFULL!')
      return rsp
    except Exception as e:
      print("OPEN_AI API PROMPTED FAILED!:", e)
