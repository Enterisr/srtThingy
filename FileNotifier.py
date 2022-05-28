from concurrent.futures import process
import os
from pathlib import Path
import shutil
from VideoEditor import VideoEditor
import logging
import sys

logging.basicConfig(level=logging.INFO, filename="subsWriter.log",format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
PATH = "C:\\Users\\Drunktolstoy\\Videos"
EXCEPTABLE_EXTENSIONS = ["mp4"]
CACHE_FILE = "movies.txt"
class FileNotifier:

    def __init__(self,path=PATH):
        self.path = path
        self.existing_movies = []
        try:
            with open(CACHE_FILE,"r+") as exisiting_movies:
                    self.existing_movies = exisiting_movies.readlines()
        except FileNotFoundError:
            with open(CACHE_FILE,"w") as file:
                file.write('')

    def write_new_videos_to_file(self,new_videos):
         with open(CACHE_FILE,"a+t") as exisiting_movies:
            for video in new_videos:
                _video = video+"\n"
                exisiting_movies.write(_video)

    def get_new_videos(self,path=None):
        if path==None:
            path = self.path
        new_videos = []
        for root,dirs,files in os.walk(path):
            for name in files:
                file_with_path = os.path.join(root, name)
                if file_with_path+'\n' not in self.existing_movies and self.check_if_valid_extension(name):
                    new_videos.append(file_with_path)
                    logger.info("found new movie: "+ file_with_path)
            for dir in dirs:
                new_videos_from_dir = self.get_new_videos(dir)
                new_videos.extend(new_videos_from_dir)
        return new_videos
    
    def check_if_valid_extension(self, file:str):
        for exntension in EXCEPTABLE_EXTENSIONS:
            if file.endswith(exntension) and file.count("__subbed__") == 0:
                return True
        return False

    def search_subtitles_in_folder(self, file_path) -> str:
        dir_of_file = Path(file_path).parent
        files_of_dir = os.listdir(dir_of_file)
        for file in files_of_dir:
            if file.endswith(".srt"):
                logger.log(f"Found subtitles for {self.file} in own directory")
                old_path = str(Path.joinpath(dir_of_file, file))
                new_path = os.getcwd() +"\\"+ file;
                shutil.copy(old_path,new_path)
                return file
        return None

if __name__ == "__main__":
    notifier = FileNotifier()
    new_videos = notifier.get_new_videos()
    notifier.write_new_videos_to_file(new_videos)
    for video in new_videos:
        editor = VideoEditor(video)
        video.replace("\n","")
        subs_name = notifier.search_subtitles_in_folder(video)
        if subs_name is None:      
            subs_name = editor.fetch_subtitles()
        editor.add_subtitles(video, subs_name)
        os.system('TASKKILL /F /IM ffmpeg.exe')
        os.remove(subs_name)
        
