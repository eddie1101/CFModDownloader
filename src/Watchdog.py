import time, logging, shutil, os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


LOGGER_NAME = "Watchdog Log"


class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler(), logger = logging.getLogger(LOGGER_NAME)):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory
        self.logger = logger

    def run(self):
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        self.logger.log(logging.DEBUG, "\nWatchdog Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        self.logger.log(logging.DEBUG, "\nWatchdog Terminated\n")


class DownloadHandler(FileSystemEventHandler):

    def __init__(self, target_dir, logger = logging.getLogger(LOGGER_NAME)):
        super().__init__()
        self.target_dir = target_dir
        self.logger = logger
        self.mods_dir = target_dir + "/mods"
        self.resourcepacks_dir = target_dir + "/resourcepacks"
    
    def on_created(self, event):
        src = event.src_path
        self.logger.log(logging.DEBUG, src)

        #Move file to appropriate folder based on whether it is a mod or resource pack
        if src.endswith(".zip") or src.endswith(".jar"):
            shutil.move(src, self.mods_dir if src.endswith(".jar") else self.resourcepacks_dir)


def start_watchdog_thread(install_dir, downloads_dir, logger):
    Watcher(downloads_dir, DownloadHandler(install_dir, logger), logger).run()