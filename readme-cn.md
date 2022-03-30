
<p align="center"><a href="https://github.com/neargle/crx-scouter" target="_blank" rel="noopener noreferrer"><img height="100" src="img/favicon.svg.png" alt="Vue logo"><img height="100" src="img/title.png" alt="Vue logo"></a></p>

crx-scouter.js 基于前端指纹可以探测到我们正在使用哪些 Chrome 插件(扩展)，可以检测电脑那端的人是帅气的大黑客还是高端的程序员🐱，被用于蜜罐、人机识别、用户画像、广告屏蔽对抗、插件漏洞利用的前置检查等场景:

* Chrome的安全设计在这五年间有了新的变化，Google视乎想解决这个问题，但是收效甚微，2021年对Chrome相关特性的分析可以阅读 [《点我的链接我就能知道你用了哪些 chrome 插件 - IN 2021》](https://github.com/neargle/crx-scouter#In-2021)
* 📚 检测原理可参考我们2016年的文章，他有一个符合乌云时代的名字: [《点我的链接我就能知道你用了哪些 chrome 插件》](https://github.com/neargle/crx-scouter#%E7%82%B9%E6%88%91%E7%9A%84%E9%93%BE%E6%8E%A5%E6%88%91%E5%B0%B1%E8%83%BD%E7%9F%A5%E9%81%93%E4%BD%A0%E7%94%A8%E4%BA%86%E5%93%AA%E4%BA%9B-chrome-%E6%8F%92%E4%BB%B6)
* ✨ |・ω・｀) 在线检测地址: [https://blog.neargle.com/crx-scouter/](https://blog.neargle.com/crx-scouter/)
* 一些指引
    - 📚 <a class="title-link" href="https://github.com/neargle/crx-scouter/tree/master" rel="nofollow" target="_blank"> Crawler Source Code </a>
    - 🆕 <a class="title-link" href="https://github.com/neargle/crx-scouter/issues/new?assignees=&labels=&template=bug-report.md" rel="nofollow" target="_blank">Request A New Fingerprint </a>

## HOW TO USE

crx-scouter.js 支持只检测单个插件，只需传入插件ID和回调函数如下：

```javascript
const { check_one } = await import('./scouter/scouter')
check_one("aapbdbdomjkkjkaonfhkkikfgjllcleb", console.log)
```

`console.log` 回调输出下列信息则表示当前浏览器使用了 Google Translate 插件。
```json
{
    "extid": "aapbdbdomjkkjkaonfhkkikfgjllcleb",
    "url": "https://chrome.google.com/webstore/detail/google-translate/aapbdbdomjkkjkaonfhkkikfgjllcleb",
    "name": "Google Translate"
}
```

当然也有支持检测指纹中的所有插件的函数 `check_all_crx(callback)`， [✨ 在线检测地址](https://blog.neargle.com/crx-scouter/) 就基于这个函数，效果图如下：

![image](https://user-images.githubusercontent.com/7868679/144161050-21a9f375-7c02-4cf4-820a-6072cb0de237.png)

## In 2021

[WIP]


## [检测原理] 点我的链接我就能知道你用了哪些 chrome 插件

注⚠️：这个是2016年发布在 n0tr00t 上的报告/博客原文，由于 n0tr00t 的师傅们已不再运营，故在此备份，工具和数据的说明请跳转到[参考之后](#参考)。

咳咳，我知道干货一般阅读量会比较低，所以我借用了安全圈段子讲的最好的人惯用的漏洞标题风格。  

由安全研究员 evi1m0 和 neargle 挖掘并编写 poc，测试链接在文末。

#### **0x01 About**

编写过 Chrome 扩展的开发人员都应该清楚在 crx 后缀的包中， manifest.json 配置清单文件提供了这个扩展的重要信息，crx 后缀文件可以直接使用 unzip 解压，Windows 下的安装后解压的路径在：C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Extensions ，MacOS 在：cd ~/Library/Application\ Support/Google/Chrome/Default/Extensions ，其中 manifest.json 的样例：

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

可以看到关于这个扩展的 content_scripts, desc, homepage, icons 等等配置信息，其中 manifest_version 字段标明现在的 rule 为 2.0 版本，在 2012 年 Chrome 便将 1.0 manifest.json 配置版本的扩展禁止新建在应用市场中，但允许更新，直到 2014 年彻底禁用所有的 version 1.0 版本扩展 / 应用并更新至 2.0，其中一大部分原因是由于新版规则上安全性的提升。

#### **0x02 Manifest**

* 2.0 中关于 CSP 的强制应用，要求开发者配置 content_security_policy ，如果未设置的话则使用 Chrome 的默认 manifest csp 规则；
* 不同于老版本的规则，crx 下的资源文件不再是默认可用（直接访问）的图像、资源、脚本。如果想让网站能够加载其资源就必须配置 web_accessible_resources 清单；
* 删除 chrome.self API ，使用 chrome.extension 替代；
* ...

#### **0x03 script <–> onload / onerror**

在多年前的 ChromeExtensions 探测中我们可以直接探测静态资源文件来判断是否存在，在上面的更新变动中可以看到，如果访问资源则必须在 web_accessible_resources 中声明 LIST （可以使用通配符），拿 json-view 举例：

```json
"web_accessible_resources": [ "assets/options.html", "assets/csseditor.html", "assets/css/jsonview.css", "assets/css/jsonview-core.css", "assets/css/content_error.css", "assets/images/options.png", "assets/images/close_icon.gif", "assets/images/error.gif" ]
```

访问他们资源的 URL 格式如下：

```js
'chrome-extension://' + id + web_accessible_resources
```

在测试的过程中我们发现大量的扩展禁止了 iframe 内嵌访问，这里我们可以使用 script 加载页面的差异化来判断是否存在文件：

```html
<script src="chrome-extension://aimiinbnnkboelefkjlenlgimcabobli/assets/options.html" onload="alert('json-view!')" onerror="alert(':(')"></script>
```

![](http://mmbiz.qpic.cn/mmbiz_jpg/PAV8ewtdsKo4nQzgLy4icPNkrSgCzFAztNOzgMRxVcoLqPicUkf1RHcNehV0vwCcBwFRRhiceje8lC8rzdmgeDH5w/0?wx_fmt=jpeg)

#### **0x04 Chrome Extensions Spider**

我们编写了爬虫获取整个[谷歌商店](https://chrome.google.com/webstore/category/extensions?hl=en-US)中的扩展应用（id, name, starts, users, category, url），分类如下：

```python
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
```

截至 2017 年初 谷歌商店扩展应用总数量为 42658 ，我们将这些 crx 全部进行下载分析其 manifest.json 的编写规则，**发现 12032 个扩展可以探测**，**在之后的实际测试过程中也发现探测应用的成功率为 1/3 ~ 1/4** ，比较客观，保存的 JSON 格式如下：

```json
{
  "web_accessible_resources": [
    "19.png",
    "48.png",
    "i/4000.png"
  ],
  "name": "Facepad for Facebook\u2122",
  "stars": 497,
  "id": "cgaknhmchnjaphondjciheacngggiclo",
  "url": "https://chrome.google.com/webstore/detail/facepad-for-facebook/cgaknhmchnjaphondjciheacngggiclo",
  "category": "ext/10-blogging",
  "users": "11,686"
},
{"web_accessible_resources": ["reload.js"], "name": "Refresh for Twitter", "stars": 184, "id": "hdpiilkeoldobfomlhipnnfanmgfllmp", "url": "https://chrome.google.com/webstore/detail/refresh-for-twitter/hdpiilkeoldobfomlhipnnfanmgfllmp", "category": "ext/10-blogging", "users": "31,796"
},
{
"web_accessible_resources": ["main.css", "lstr.js", "script.js", "images/close.png", "images/back.png", "images/icon19.png", "images/play.png", "images/stop.png", "images/prev.png", "images/down.png", "images/next.png", "images/delete.png", "classes/GIFWorker.js"], "name": "MakeGIF Video Capture", "stars": 309, "id": "cnhdjbfjheoohmhpakglckehdcgfffbl", "url": "https://chrome.google.com/webstore/detail/makegif-video-capture/cnhdjbfjheoohmhpakglckehdcgfffbl", "category": "ext/10-blogging", "users": "55,360"
},
{
"web_accessible_resources": ["js/move.js"], "name": "Postagens Megafilmes 2.1", "stars": 0, "id": "ekennogbnkdbgejohplipgcneekoaanp", "url": "https://chrome.google.com/webstore/detail/postagens-megafilmes-21/ekennogbnkdbgejohplipgcneekoaanp", "category": "ext/10-blogging", "users": "2,408"
},
```

#### **0x05 ProbeJS**

通过编写脚本可以加载并探测本地扩展是否存在，虽然需要触发大量的请求来探测，但由于是访问本地资源其速度仍然可以接受，我们过滤出 **users 1000 以上的扩展**来进行筛选探测（ testing 函数动态创建并删除不成功的 dom 探测节点）：

```js
$.get("ext1000up.json" + "?_=" + new Date().valueOf(), function(ext){
    for (let n in ext.data) {
        var id = ext.data[n].id;
        var name = ext.data[n].name;
        var war = ext.data[n].web_accessible_resources;
        var curl = ext.data[n].url;
        testing(id, name, war, curl);
    }
    $('#loading').remove();
})
```

![](http://mmbiz.qpic.cn/mmbiz_jpg/PAV8ewtdsKo4nQzgLy4icPNkrSgCzFAzt4LaMPolcFsz8xmg2NuymAf8nkibuwClDibc9dEkuzKeqHt6eOruZMUww/0?wx_fmt=jpeg)

## Thanks

* @evi1m0 - 天才黑客少年，现在转行卖小裙子了，多糖CEO
* @phith0n - 我已经忘记五年前和P师傅做啥事了，但依然感谢
* @Nikaple - 腾讯支付业务前端工程师
