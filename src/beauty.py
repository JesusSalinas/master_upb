import requests
import re

from bs4 import BeautifulSoup
from data.objs import data

class BeautySoapScrap:
    """ This Class """

    def __init__(self):
        self.body=None
        self.err=None

    async def valid_host(self, host):
        """ This Function """
        base_url = host
        try:
            response = requests.get(base_url)
            if response.status_code == 200:
                print("FETCH HOST SUCCESSFULL!")
                rsp = response.content
                self.body = self.get_data(rsp)
                return True
            else:
                print("FETCH HOST FAILED!")
                self.err = 'RESPONSE STATUS CODE:' + str(response.status_code)
                return False
        except Exception as e:
            print("FETCH HOST FAILED!:", str(e))
            self.err = str(e)
            return False
        
    def get_data(self, body):
        """ This Function """
        if body:
            html = BeautifulSoup(body, "html.parser")
            data['title'] = html.find("h1").text.strip()
            bullets = html.select("main li")
            for li in bullets:
                txt = li.text.strip()
                data['bullets'].append(txt)
            paragraphs = html.select("main p")
            for p in paragraphs:
                txt = p.text.strip()
                data['paragraphs'].append(txt)
            print(data['title'])
            return data
        else:
            print("FETCH self.body FAILED!:")
            return False

    def clean_txt(self, txt_raw):
        all_txt = ""
        for obj in txt_raw:
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

        return all_txt