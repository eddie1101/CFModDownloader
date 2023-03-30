import sys, json, os, requests, re
import webbrowser as web

from bs4 import BeautifulSoup


def get_CFL_HTML(projectID, fileID):
    r = requests.get(f'https://cflookup.com/{projectID}?fileId={fileID}')
    if r.status_code == 200:
        return r.text
    else:
        return None


def get_CF_slug(projectID, fileID):
    html = get_CFL_HTML(projectID, fileID)
    if html is None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        url = link.get('href')
        if url.startswith('https://') and '/mc-mods/' in url:
            return url.split('/')[-1]


def main():
    j = None
    try:
        j = json.loads(open('manifest.json', 'r').read())
    except:
        print("Manifest not found. Make sure to place the modpack's manifest.json file in the script directory.")
        sys.exit()

    files = j['files']
    for file in files:
        projectID, fileID = file['projectID'], file['fileID'] 
        slug = get_CF_slug(projectID, fileID)
        if slug is None:
            print(f'Could not find mod:\n\tProject ID: {projectID}\n\tFile ID: {fileID}')
        else:
            download_link = f'https://www.curseforge.com/minecraft/mc-mods/{slug}/download/{fileID}'
            print(f'Downloading {slug} ({download_link})...')
            web.open(download_link)

if __name__ == '__main__':
    main()
