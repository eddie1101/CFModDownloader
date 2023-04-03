# Curseforge Modpack Downloader

Shitty Python script to download mods given a Curseforge manifest.json.

## Purpose
Curseforge doesn't allow you to download modpacks without their bloatware and you can no longer programmatically download mods without an API key.
This solution is still (very) shitty, but IMO it's worth avoiding the mental anguish of using Overwolf and the Curseforge App.

## Set-Up
1. `pip install -r requirements.txt`
2. Place the manifest.json of the modpack you want to download in the script directory (ensure it is named exactly "manifest.json")
3. Run the script
4. (Optionally) If you use Chrome, have a lot of RAM lmao (Works much better if your browser is allowed to automatically save files)
5. Wait for downloads to finish

## Usage
`py CFModDownloader.y {Install Directory} {Daemon Duration}`
- (Optional) Install Directory: The path to where you want the modpack files to be saved to
- (Optional) Daemon Duration: How long (in seconds) the daemon which moves downloads into the install directory will stay awake for. If you have slow download speeds, set to a higher number. Install directory argument must be present. Default 10.

## Disclaimer
This is a terrible way to do this. It could be improved but I don't care. It may be faster than downloading the mods manually, but at what cost?
Be aware that if you're downloading a modpack with 300 mods, this script will open 300 browser tabs :/

I spent maybe 10 minutes on this. If it doesn't work, sorry ¯\\_(ツ)_/¯

It also might not work at all if [CFLookup](https://cflookup.com/) changes.
