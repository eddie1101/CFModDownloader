import sys, json, os, requests, re
import webbrowser as web

from bs4 import BeautifulSoup


def get_CFL_HTML(projectID, fileID):
    r = requests.get(f'https://cflookup.com/{projectID}?fileId={fileID}')
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
        html = get_CFL_HTML(projectID, fileID)
        slug = get_CF_slug(html)
        if slug is None:
            print(f'Could not find mod. Try plugging these numbers into www.cflookup.com:\n\tProject ID: {projectID}\n\tFile ID: {fileID}')
        else:
            download_link = f'https://www.curseforge.com/minecraft/{"texture-packs" if slug[1] else "mc-mods"}/{slug[0]}/download/{fileID}'
            print(f'Downloading {slug[0]} ({download_link})...')
            web.open(download_link)


if __name__ == '__main__':
    main()

