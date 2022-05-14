import os

from VideoEditor import VideoEditor

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
                if name+"\n" not in self.existing_movies and self.check_if_valid_extension(name):
                    new_videos.append(name)
            for dir in dirs:
                new_videos_from_dir = self.get_new_videos(dir)
                new_videos.extend(new_videos_from_dir)
        return new_videos
    
    def check_if_valid_extension(self, file:str):
        for exntension in EXCEPTABLE_EXTENSIONS:
            if file.endswith(exntension):
                return True
        return False


if __name__ == "__main__":
    notifier = FileNotifier()
    new_videos = notifier.get_new_videos()
    notifier.write_new_videos_to_file(new_videos)
    for video in new_videos:        
        editor = VideoEditor(video)
        
