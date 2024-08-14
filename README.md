# Curseforge Modpack Downloader

Shitty Python script to download mods given a Curseforge manifest.json.

## Purpose
Curseforge doesn't allow you to download modpacks without their bloatware and you can no longer programmatically download mods without an API key.
This solution is still (very) shitty, but IMO it's worth avoiding the mental anguish of using Overwolf and the Curseforge App.

## Set-Up
1. Set firefox as your default browser (this only works with firefox. Other browsers are too slow and cannot handle the hundreds of tabs that this script opens)
2. (Optional, but highly recommended) Install the uBlock Origin extension for firefox.
3. Install python 3.9 (recommended to create a venv)
4. `pip install -r requirements.txt`
5. Run the script (see [Usage](#usage) below)
6. Wait for downloads to finish

## Usage
`py CFModDownloader.py modpack-zip {-i Install-Directory} {-d Watchdog-Duration}`
- modpack-zip: The path to the modpack .zip downloaded from CurseForge.
- (Optional) Install-Directory: The path to where you want the modpack files to be saved to.
- (Optional) Watchdog-Duration: How long (in seconds) the daemon which moves downloads into the install directory will stay awake for. If you have slow download speeds, set to a higher number. Install directory argument must be present. Default 30.

Always use absolute paths.

## Disclaimer
This is a terrible way to do this. It could be improved but I don't care. It may be faster than downloading the mods manually, but at what cost?
Be aware that if you're downloading a modpack with 300 mods, this script will open 300 browser tabs :/

I spent maybe a couple hours on this. If it doesn't work, sorry ¯\\_(ツ)_/¯

It also might not work at all if [CFLookup](https://cflookup.com/) changes.

Excessive usage may cause Curseforge to prompt you with a captcha, blocking further downloads until completed. 

Tested on Windows 10 with Python 3.10
