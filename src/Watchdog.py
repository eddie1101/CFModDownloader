import time, logging, shutil, os, threading, _thread as thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


LOGGER_NAME = "Watchdog Log"

class Watchdog(threading.Thread):

    def __init__(self, directory=".", handler=FileSystemEventHandler(), logger = logging.getLogger(LOGGER_NAME)):
        super().__init__()
        self.observer = Observer()
        self.handler = handler
        self.directory = directory
        self.logger = logger
        self.stop_flag = False

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        self.logger.log(logging.DEBUG, "\nWatchdog Running in {}/\n".format(self.directory))
        try:
            while not self.stop_flag:
                time.sleep(1)
            self.logger.log(level=logging.DEBUG, msg="Watchdog Received Stop Signal\n")
        except:
            pass
        self.observer.stop()
        self.observer.join()
        # while(self.observer.is_alive()):
        #     time.sleep(0.5)
        #     self.logger.log(level=logging.DEBUG, msg="\nWaiting for Observer to Join\n")
        self.logger.log(level=logging.DEBUG, msg="Watchdog Terminated\n")

    def stop(self):
        self.stop_flag = True  


class DownloadHandler(FileSystemEventHandler):

    def __init__(self, target_dir, logger = logging.getLogger(LOGGER_NAME)):
        super().__init__()
        self.target_dir = target_dir
        self.logger = logger
        self.mods_dir = target_dir + "/mods"
        self.resourcepacks_dir = target_dir + "/resourcepacks"
    
    def on_created(self, event):
        src = event.src_path

        #Move file to appropriate folder based on whether it is a mod or resource pack
        if src.endswith(".zip") or src.endswith(".jar"):
            dst = self.mods_dir if src.endswith(".jar") else self.resourcepacks_dir
            self.logger.log(level=logging.DEBUG, msg='Watchdog found: %s, moving to %s' %(src.split('\\')[-1], dst))
            thread.start_new_thread(move_file, (src, dst))


def move_file(src, dst):
    #Give time for the system to finalize download and relinquish lock
    file_size = -1
    while file_size != os.path.getsize(src):
        file_size = os.path.getsize(src)
        time.sleep(10)
    shutil.move(src, dst)
