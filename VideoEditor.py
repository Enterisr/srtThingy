import ffmpeg
import requests
import os
import json
from dotenv import load_dotenv
import logging
import sys

load_dotenv()
URL = "https://api.opensubtitles.com/api/v1/subtitles?languages=en,he"
DOWNLOAD_LINK_REQ = "https://api.opensubtitles.com/api/v1/download"
headers = { 'Content-Type': 'application/json', "Api-Key": os.getenv("API_KEY") }
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

generator = lambda txt:TextClip(txt, font='Arial', fontsize=24, color='white')

class VideoEditor:
    
    def __init__(self, file):
        self.file = os.path.basename(file)

    def fetch_subtitles(self) -> str:
        PARAMS = {"query":self.file}
        r = requests.get(url=URL,params=PARAMS,headers=headers)
        srt_file_obj = r.json()["data"][0]["attributes"]["files"][0]
        srt_file_name = srt_file_obj["file_name"]
        srt_file_id = srt_file_obj["file_id"]
        logger.info(f"Found subtitles for {self.file}: {srt_file_name} in open subtitles")
        body = {"file_id" : srt_file_id}
        download_url = requests.post(DOWNLOAD_LINK_REQ, data=json.dumps(body), headers=headers).json()["link"]
        with open(srt_file_name, "wt") as srt_file:
            downloaded_file = requests.get(download_url).text
            srt_file.write(downloaded_file)
        return srt_file_name

    def add_subtitles(self,file_path:str, subs_file:str):
        try:
            new_file_name = file_path.replace(".mp4","__subbed__.mp4")
            #todo: do this with subtitles, use gpu 
            video = ffmpeg.input(file_path)
            audio = video.audio
            ffmpeg.concat(video.filter("subtitles", subs_file), audio, v=1, a=1).output(new_file_name).run()
        except Exception as e:
            logger.error(f"there was an error while trying to stick {subs_file} to {file_path}")
            logger.error(e)

