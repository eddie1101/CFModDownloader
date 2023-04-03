import sys, json, os, requests, re
import webbrowser as web

from bs4 import BeautifulSoup


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


def main():
    j = None
    try:
        with open('manifest.json', 'r') as manifest:
            j = json.loads(manifest.read())
    except:
        print("Manifest not found. Make sure to place the modpack's manifest.json file in the script directory.")
        sys.exit()

    files = j['files']
    for file in files:
        project_id, file_id = file['projectID'], file['fileID']
        html = get_CFL_HTML(project_id, file_id)
        slug = get_CF_slug(html)
        if slug is None:
            print(f'Could not find mod. Try plugging these numbers into www.cflookup.com:\n\tProject ID: {project_id}\n\tFile ID: {file_id}')
        else:
            download_link = f'https://www.curseforge.com/minecraft/{"texture-packs" if slug[1] else "mc-mods"}/{slug[0]}/download/{file_id}'
            print(f'Downloading {slug[0]} ({download_link})...')
            web.open(download_link)


if __name__ == '__main__':
    main()

