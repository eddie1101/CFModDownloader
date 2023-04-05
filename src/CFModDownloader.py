import sys, json, requests, os, time, zipfile, shutil, argparse
import webbrowser as web
import logging
from threading import Thread
from pathlib import Path

from bs4 import BeautifulSoup

from Watchdog import Watchdog, DownloadHandler, LOGGER_NAME


def get_CFL_HTML(project_id, file_id):
    r = requests.get(f'https://cflookup.com/{project_id}?fileId={file_id}')
    if r.status_code == 200:
        return r.text
    else:
        return None


def get_CF_slug(html):
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('https://') and ('/mc-mods/' in url or '/texture-packs/' in url):
            return (url.split('/')[-1], True if '/texture-packs/' in url else False)
        

def check_dirs(install_dir):
    if not os.path.exists(install_dir):
        os.mkdir(install_dir)
    
    mods_dir = install_dir + "/mods"
    if not os.path.exists(mods_dir):
        os.mkdir(mods_dir)

    resourcespacks_dir = install_dir + "/resourcepacks"
    if not os.path.exists(resourcespacks_dir):
        os.mkdir(resourcespacks_dir)

    if not os.path.exists('../temp'):
        os.mkdir('../temp')

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('modpack_path')
    parser.add_argument('-i', '--install')
    parser.add_argument('-d', '--duration', type=int, default=30)

    args = parser.parse_args()

    modpack_path = args.modpack_path
    install_path = args.install
    watchdog_duration = args.duration

    watchdog = None
    if install_path is not None:
        #Start watchdog to move downloads into install directory
        check_dirs(install_path)

        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)

        downloads_dir = str(Path.home() / "Downloads")

        download_handler = DownloadHandler(install_path, logger)
        watchdog = Watchdog(downloads_dir, download_handler, logger)
        watchdog.start()
    #Else, run in dumb mode, let the user handle the downloads

    #Extract manifest.json and overrides
    with zipfile.ZipFile(modpack_path, 'r') as zip:
        zip.extractall('../temp')

    #Extract file IDs from manifest.json
    j = None
    try:
        with open('../temp/manifest.json', 'r') as manifest:
            j = json.loads(manifest.read())
    except ValueError as ve:
        print("Manifest is malformed. Did you bungle it up somehow?")
        sys.exit()
    except FileNotFoundError as fnfe:
        print("Manifest not found. Are you sure you provided the path to the right zip file?")
        sys.exit()

    #Retrieve file IDs and project IDs
    files = j['files']
    for file in files:
        project_id, file_id = file['projectID'], file['fileID']
        #Get html from cflookup.com
        html = get_CFL_HTML(project_id, file_id)
        #Scrape html for project slug
        slug = get_CF_slug(html)
        if slug is None:
            print(f'Could not find mod. Try plugging these numbers into www.cflookup.com:\n\tProject ID: {project_id}\n\tFile ID: {file_id}')

        #Construct download link from project slug and file ID, and open in browser to start automatic download
        else:
            download_link = f'https://www.curseforge.com/minecraft/{"texture-packs" if slug[1] else "mc-mods"}/{slug[0]}/download/{file_id}'
            print(f'Downloading {slug[0]} ({download_link})...')
            web.open(download_link)
                

    #Copy overrides into installation
    if install_path is not None:
        overrides_dir = os.path.abspath('../temp/overrides')
        for src_dir, dirs, files in os.walk(overrides_dir):
            dst_dir = src_dir.replace(overrides_dir, install_path, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy(src_file, dst_dir)

    shutil.rmtree('../temp')
    
    #Countdown watchdog sleep (hopefully everything will be done downloading by then)
    if watchdog is not None:
        for x in range(watchdog_duration):
            print(f'Watchdog will continue monitoring for downloads for ({watchdog_duration - (x + 1)}) seconds. Press ctrl+C to end now.', end='\r')
            time.sleep(1)
        watchdog.stop()
        watchdog.join()

    print()

if __name__ == '__main__':
    main()

