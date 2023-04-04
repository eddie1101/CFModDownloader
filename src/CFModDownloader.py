import sys, json, requests, os, time, zipfile, shutil
import webbrowser as web
import logging
from threading import Thread
from pathlib import Path

from bs4 import BeautifulSoup

from Watchdog import start_watchdog_thread, LOGGER_NAME


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


def main():

    watchdog, daemon_duration = None, 10
    if len(sys.argv) > 2:
        #Start watchdog to move downloads into install directory
        install_dir = sys.argv[2]
        check_dirs(install_dir)
        downloads_dir = str(Path.home() / "Downloads")
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        watchdog = Thread(target=start_watchdog_thread, args=(install_dir, downloads_dir, logger), daemon=True, name="Watchdog")
        watchdog.start()

        if len(sys.argv) > 3:
            daemon_duration = int(sys.argv[2])
    #Else, run in dumb mode, let the user handle the downloads

    #Extract manifest.json and overrides
    with zipfile.ZipFile(sys.argv[1], 'r') as zip:
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
        print("Manifest not found. Make sure to place the modpack's manifest.json file in the script directory.")
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

    overrides_dir = '../temp/overrides'
    overrides = os.listdir(overrides_dir)
    for o in overrides:
        shutil.move(overrides_dir + f'/{o}', install_dir)
    
    #Countdown watchdog sleep (hopefully everything will be done downloading by then)
    if watchdog is not None:
        for x in range(daemon_duration):
            print(f'Watchdog will continue monitoring for downloads for ({daemon_duration - (x + 1)}) seconds. Press ctrl+C to end now.', end='\r')
            time.sleep(1)
    # watchdog.join()
    print()

if __name__ == '__main__':
    main()

