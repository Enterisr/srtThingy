import ffmpeg
import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()
URL = "https://api.opensubtitles.com/api/v1/subtitles"
DOWNLOAD_LINK_REQ = "https://api.opensubtitles.com/api/v1/download"
headers = { 'Content-Type': 'application/json', "Api-Key": os.getenv("API_KEY") }

generator = lambda txt:TextClip(txt, font='Arial', fontsize=24, color='white')

class VideoEditor:
    
    def __init__(self,file):
        self.file = file
        PARAMS = {"query":file}
        r = requests.get(url=URL,params=PARAMS,headers=headers)
        srt_file = r.json()["data"][0]["attributes"]["files"][0]
        srt_file_name = srt_file["file_name"]
        srt_file_id = srt_file["file_id"]
        print(f"Found subtitles for {file}: {srt_file_name}")
        body = {"file_id" : srt_file_id}
        download_url = requests.post(DOWNLOAD_LINK_REQ, data=json.dumps(body), headers=headers).json()
        print(download_url)

    """def add_subtitles(self,file:str):
        ffmpeg
        .input(file)
        .filter("subtitles", "")"""

    #fetch_subtitles(self,)

