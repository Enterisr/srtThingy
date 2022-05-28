import subprocess
import socket
import os
TASK_NAME = "SubsWriter"



class ServiceRegisterer():
    def __init__(self):
        read = subprocess.check_output("schtasks")
        is_task_created = read.decode().find(TASK_NAME)
        if is_task_created == -1:
            subprocess.run(["schtasks","/create","/XML",TASK_NAME+".xml","/tn",TASK_NAME,"/ru",f'{socket.gethostname()}\{os.getlogin()}',"/rp"])
            return
        print("task already exists")
        



if __name__ == "__main__":
    ServiceRegisterer()
