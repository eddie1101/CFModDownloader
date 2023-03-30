# Curseforge Modpack Downloader

Shitty Python script to download mods given a Curseforge manifest.json.

## Purpose
Curseforge doesn't allow you to download modpacks without their bloatware and you can no longer programmatically download mods without an API key.
This solution is still (very) shitty, but IMO it's worth avoiding the mental anguish of using Overwolf and the Curseforge App.

## Usage
1. `pip install -r requirements.txt`
2. Place the manifest.json of the modpack you want to download in the script directory (ensure it is named exactly "manifest.json")
3. Run the script
4. (Optionally) If you use Chrome, have a lot of RAM lmao

## Disclaimer
This is a terrible way to do this. It could be improved but I don't care. It may be faster than downloading the mods manually, but at what cost?
Be aware that if you're downloading a modpack with 300 mods, this script will open 300 browser tabs :/

I spent maybe 10 minutes on this. If it doesn't work, sorry ¯\\_(ツ)_/¯

It also might not work at all if [CFLookup](https://cflookup.com/) changes.
