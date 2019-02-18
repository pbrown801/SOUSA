# Installing GalliumOS
GalliumOS installation on Braswell Chromebook

___
## Prepping your Chromebook for Installation


**The following installation guide has the potential to brick your device. Make sure you follow directions as closely as possible to minimize this risk. If it is bricked, there are easy-to-follow guides online to help with fixing this**

### Removing the Write-Protection

1. Make sure the device is powered off and unscrew the back
2. There should be a screw with a "WP" or a white arrow somewhere near it. Unscrew this. Keep it if you want, but I didn't. Your device is now "unlocked" and the firmware can be replaced.
3. Reattach the back.
### Replacing Firmware
1. Boot into developer mode. You'll do this by pressing ESC-Refresh-Power. When the warning screen pops up, press CTRL-D and then Enter at the prompt.
2. When you're at the home screen, press CTRL+ALT+T and type `shell` to pull up a bash shell.
3. `cd; curl -LO https://mrchromebox.tech/firmware-util.sh && sudo bash firmware-util.sh` This will download the firmware installation script.
4. We'll be doing a Full ROM installation, so when the script is run, you'll pick option 3. I've provided a copy of your ChromeOS firmware in the SOUSA repository. 

**Up until this point, we've been following instructions on [this site](https://mrchromebox.tech/#fwscript)
### Installing GalliumOS
For our device, the main release doesn't have keyboard functionality. So we'll use a pre-release that, as far as I'm concerned, works fine. You can download that [here](https://galliumos.org/releases/nightly/galliumos-braswell-xenon-20171227T072217Z.iso).
1. You'll need to have a clean flash drive to perform the installation.
2. Follow the instructions on [this page](https://wiki.galliumos.org/Installing/Creating_Bootable_USB) to create a bootable drive. You'll follow the macOS Traditional instructions.
3. Plug in your drive to the Chromebook and boot. When you're at the boot screen, you'll press ESC and navigate to boot from the USB device.

**At this point, you have not installed GalliumOS on your Chromebook. You are simply running it from the flash drive.**

4. When given the option, you can install by clicking the GalliumOS icon on the desktop. After this, you won't have to have the flash drive inserted to run the OS and it should function on its own.

Test to make sure everything works (keyboard, sound, etc.)

### Provided below are URLs to common problems I ran into and their solutions:
* [Boot to console on Chromebook](https://old.reddit.com/r/GalliumOS/comments/aglzac/boot_to_console/)
* [Delete Ubuntu user](https://stackoverflow.com/questions/28103045/how-can-i-delete-a-user-in-linux-when-the-system-says-its-currently-used-in-a-pr)
* [Set or Change User Password](https://www.cyberciti.biz/faq/linux-set-change-password-how-to/)
* [Installing GSettings (needed for software install later)](https://launchpad.net/ubuntu/xenial/+package/libglib2.0-bin)

That should be all! If you followed all the instructions you should have a standalone GalliumOS installation on a Chromebook. 
# Security
For security purposes, I recommend Firefox as a web browser. To disable telemetry (data reporting to Mozillia) follow [this guide](https://www.downloadsource.net/how-to-turn-off-telemetry-and-data-collection-on-firefox-quantum/n/11372/).
Additionally, you should install the following add-ons:

1. [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/?src=search)
2. [DuckDuckGo](https://addons.mozilla.org/en-US/firefox/addon/duckduckgo-for-firefox/)
3. [HTTPS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/)
4. [NoScript](https://addons.mozilla.org/en-US/firefox/addon/noscript/) (this will disable JavaScript on sites by default. If you trust the site, temporarily enable it. Don't enable Google analytics or anything tracking related.)
5. I'd use DuckDuckGo as your primary search engine. They use Google results, but don't track you like Google does.

# Troubleshooting
If something is going wrong and a DuckDuckGo search can't solve it, feel free to contact me at:

Tate Walker: 
tatewalker@tamu.edu