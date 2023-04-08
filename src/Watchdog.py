import time, logging, shutil, os, threading, _thread as thread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


LOGGER_NAME = "Watchdog Log"

class Watchdog(threading.Thread):

    def __init__(self, directory, handler, logger):
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
            self.logger.log(level=logging.DEBUG, msg="\nWatchdog Received Stop Signal\n")
        except:
            pass
        self.observer.stop()
        self.observer.join()
        self.logger.log(level=logging.DEBUG, msg="Watchdog Terminated\n")

    def stop(self):
        self.stop_flag = True  


class DownloadHandler(FileSystemEventHandler):

    def __init__(self, target_dir, logger):
        super().__init__()
        self.target_dir = target_dir
        self.logger = logger
        self.mods_dir = target_dir + "/mods"
        self.resourcepacks_dir = target_dir + "/resourcepacks"
    
    def on_created(self, event):
        src = event.src_path
        if src.endswith('.jar') or src.endswith('.zip'):
            dst = self.mods_dir if src.endswith('.jar') else self.resourcepacks_dir
            self.logger.log(level=logging.DEBUG, msg=f'Watchdog found: {src} | Moving to installation folder when download is complete.')
            thread.start_new_thread(self.move_file_timer, (src, dst))

    def move_file_timer(self, src, dst):
        #Give time for the browser to finalize and flush download buffer
        while os.path.getsize(src) == 0:
            time.sleep(2)
        shutil.move(src, dst)
