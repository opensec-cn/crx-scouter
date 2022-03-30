
<p align="center"><a href="https://github.com/neargle/crx-scouter" target="_blank" rel="noopener noreferrer"><img height="100" src="img/favicon.svg.png" alt="Vue logo"><img height="100" src="img/title.png" alt="Vue logo"></a></p>

[[中文文档](./readme-cn.md)]

**crx-scouter.js** can detect which Chrome extensions we are using quietly, and can detect whether the person before the browser is a awesome hacker or a high-end programmer 🐱, It can be used for honeypots, human-machine identification, countermeasures of ad blocking, pre-checks for extension exploits, and so on.

The principle of crx-scouter.js is based on an experiment I did with evi1m0 in 2017. Google seems to want to solve this problem, but with little success. Details can be found in [the principle document](#WHY).

Demo in: [https://blog.neargle.com/crx-scouter/](https://blog.neargle.com/crx-scouter/).

## HOW TO USE

Detect a specified extension

```javascript
const { check_one } = await import('./scouter/scouter')
check_one("aapbdbdomjkkjkaonfhkkikfgjllcleb", console.log)
```

The output of `console.log` like below:

```json
{
    "extid": "aapbdbdomjkkjkaonfhkkikfgjllcleb",
    "url": "https://chrome.google.com/webstore/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb",
    "name": "Google Translate"
}
```

Of course, there is also a function `check_all_crx(callback)` that supports detection of all extensions in fingerprints. 
[✨ Online Detection Demo](https://blog.neargle.com/crx-scouter/) is based on this function, and the effect is like follows:

![image](https://user-images.githubusercontent.com/7868679/144161050-21a9f375-7c02-4cf4-820a-6072cb0de237.png)

## Why

Why can we do this?

Chrome extension Developers should know that in the package with the crx suffix, the manifest.json configuration manifest file provides important information of the extension.
The crx suffix file can be directly decompressed with unzip. Example of manifest.json like below:

```json
{
  "background": {
    "scripts": [ "background.js" ]
  },
  "content_scripts": [ {
    "all_frames": true,
    "js": [ "content.js" ],
    "matches": [ "http://*/*", "https://*/*", "ftp://*/*", "file:///*" ],
    "run_at": "document_end"
  } ],
  "description": "Validates and makes JSON documents easy to read. Open source.",
  "homepage_url": "https://github.com/teocci/JSONView-for-Chrome",
  "icons": {
    "128": "assets/images/jsonview128.png",
    "16": "assets/images/jsonview16.png",
    "48": "assets/images/jsonview48.png"
  },
  "key": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApA/pG/flimvWWAeUelHGaQ+IJajQm01JkfK0EYOJPyfsdTkHLwD3Aw16N3zuFkmwz09DcGDT+ehww7GSpW7RpbX5kHrovsqyHXtwt+a2Sp8bYFFdpRPj3+HG6366kNkwttDHMtsDkwuKaBtrQofQe5Ud9mKu9h1FDPwc2Qql9vNtvOqKFhV+EOD0vD2QlliB6sKCteu4nYBlFEkh6pYWRaXdAYSKYdE1SYIuQzE3dk11+KCaAC1T6GffL3sia8n5brVX7Qd+XtXyBzuM54w5e3STwK7uLMhLGDIzHoTcldzWUUflfwuI86VQIFBxPbvXJKqFFFno+ZHs/S+Ra2SPmQIDAQAB",
  "manifest_version": 2,
  "minimum_chrome_version": "21",
  "name": "JSON Viewer",
  "permissions": [ "clipboardWrite", "http://*/", "contextMenus", "https://*/", "ftp://*/" ],
  "short_name": "JSONViewer",
  "update_url": "https://clients2.google.com/service/update2/crx",
  "version": "0.7.0",
  "web_accessible_resources": [ "assets/options.html", "assets/csseditor.html", "assets/css/jsonview.css", "assets/css/jsonview-core.css", "assets/css/content_error.css", "assets/images/options.png", "assets/images/close_icon.gif", "assets/images/error.gif" ]
}
```

If the user needs to access the resources of the extension in the web page, he must declare LIST in web_accessible_resources, take json-view as an example:

```json
"web_accessible_resources": [ "assets/options.html", "assets/csseditor.html", "assets/css/jsonview.css", "assets/css/jsonview-core.css", "assets/css/content_error.css", "assets/images/options.png", "assets/images/close_icon.gif", "assets/images/error.gif" ]
```

The URL format for accessing these resources is like follows:

`chrome-extension://' + extension id + /assets/options.html`

I developed a crawler to get the extension application manifests in the entire Google Store,  categories like follows:
'ext/10-blogging',
'ext/15-by-google',
'ext/12-shopping',
'ext/11-web-development',
'ext/1-communication',
'ext/7-productivity',
'ext/38-search-tools',
'ext/13-sports',
'ext/22-accessibility',
'ext/6-news',
'ext/14-fun',
'ext/28-photos'
and so on.

Then, We get all extensions fingerprints that include `web_accessible_resources`.

## New in 2022

Five years later, Chrome still updated a security feature to circumvent this issue. That is, web_accessible_resources adds a matches whitelist security feature, and only URLs within the whitelist can access web_accessible_resources, avoiding front-end fingerprint detection.

***But... out of the 110,000 extensions I've crawled down this year, only 286 plugins have added the web_accessible_resources matches whitelist; and most of them are configured with `*://*/*` useless whitelists and other Clearly bypassable whitelist.***

Shows how powerless a security feature is that nobody uses or use as a wrong way.

## Thanks

* @evi1m0
* @phith0n
* @Nikaple

