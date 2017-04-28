# PROWISH

## Android app analysis

This is a pipeline for installing apps from the app store, using an automated UI on an android device, pulling the APKs from the device, and statically analysing them to detect third party libraries and hosts.

### dependencies

JDK version 1.8.0_25

### Downloading APKs via the app store

Requires root access to the android device.

1. Install android-developer-tools.
2. Get the device id `adb devices`
3. Modify `static-app-analysis/install.py` with the device id.
4. Start ADB demon as root `adb root`
5. Run `python install.py`.

APK files will be written to a directory outside the repo called apks

### Static analysis

There are two aspects to the APK analysis. Both require [APKTool](https://ibotpeaches.github.io/Apktool/). The library detection tool is `static-app-analysis/librarysearch.js`. The host detection tool is `static-app-analysis/hostsearch2.py`.

Data obtained is in `data/app-data`.

### Dynamic analysis

Can use [monkeyrunner](https://developer.android.com/studio/test/monkeyrunner/index.html) to simulate user events, or manually. Log traffic data using [mitmproxy](https://mitmproxy.org/).i

Requires Android Developer Studio tools (for monkeyrunner)

Requires rooted phone with adb root shell access, network log tool with superuser permissions.

Requires working [xray tool](https://github.com/sociam/xray). Follow instructions there to get mitmproxy running (nb: requires mitmproxy to be installed within python virtualenv).

## Web analysis

Using the [Open Web Privacy Measurement framework](https://github.com/citp/OpenWPM/).

Data obtained is in `data/web-tracking`.

## Data

Data cited in the paper is all available in `data`.