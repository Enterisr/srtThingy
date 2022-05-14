import ffmpeg
import requests
import os
from dotenv import load_dotenv


load_dotenv()
URL = "https://api.opensubtitles.com/api/v1/subtitles"
headers = { 'Content-Type': 'application/json', "Api-Key": os.getenv("API_KEY") }

generator = lambda txt:TextClip(txt, font='Arial', fontsize=24, color='white')

class VideoEditor:
    
    def __init__(self,file):
        self.file = file
        PARAMS = {"query":file}
        r = requests.get(url=URL,params=PARAMS,headers=headers)
        print(r.json()) 

    """def add_subtitles(self,file:str):
        ffmpeg
        .input(file)
        .filter("subtitles", "")"""

    #fetch_subtitles(self,)

