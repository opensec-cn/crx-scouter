Chrome WebStore Extensions Knower

---

# 参考：

http://blog.neargle.com/2017/01/09/chrome-ext-spider-for-probe/

http://server.n0tr00t.com/chrome/ext_probe.html

https://www.n0tr00t.com/2017/01/09/Chrome-Extensions-Probe.html

# 安装和运行

pip3 install -r requirements.txt

python3 geknower.py

# 帮助文档

```
$ python3 geknower.py --help                                                                             master [a41c206] modified untracked
[*] main start
Usage: geknower.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  etxDownload        This commond will Download Chrome Etx .crx...
  etxInfo            Crawl and update Chrome Etx infomation
  spec-fileCheck     Check filename in web_accessible_resources is...
  spec-weblistAgain  Re get weblist


python3 geknower.py etxDownload --outfile out.txt -f data/etx_info_all.txt -t 20 -u 10000 -p /tmp --help
[*] main start
Usage: geknower.py etxDownload [OPTIONS]

  This commond will Download Chrome Etx .crx file

Options:
  -O, --outfile TEXT    Output result a json file, default use
                        config.py:conf["etx_info_weblist_file"]
  -f, --jsonfile TEXT   Input the jsonfile as baseinfo, default use
                        config.py:conf["data_file"]
  -p, --tmppath TEXT    The program will download etx file to tmppath, default
                        use config.py:conf["tmp_path"]
  -t, --thread INTEGER  Thread number, default use config.py:conf["threadnum"]
  -d, --deltmp          del the dowload config.py:conf["del_tmp"]
  -u, --users INTEGER   Only get the users great than the number, default 0
                        get all
  --help                Show this message and exit.


$ python3 geknower.py etxInfo --help                                                                     master [a41c206] modified untracked
[*] main start
Usage: geknower.py etxInfo [OPTIONS]

  Crawl and update Chrome Etx infomation

Options:
  -O, --outfile TEXT   Output result a json file, default use
                       config.py:conf["data_file"]
  -u, --users INTEGER  Only get the users great than the number, default 0 get
                       all
  --help               Show this message and exit.


```

有几个配置的选项可以在命令行中指定，可以修改config.py修改成自己想要的配置。

## 关于config

```python
conf = {}

# 保存插件信息的文件，文件格式是每一行一个json，存储一个插件信息
conf['data_file'] = './data/data2_1000_2_1.json'

# 生成添加web_accessible_resources或者文件名列表所保存的json，这个生成会根据conf['data_file']内的插件信息进行生成
conf['etx_info_weblist_file'] = './data/test2.json'

# 用户数限制，爬取数据时只爬取用户量多余该数的插件信息
conf['more_then_user_num'] = 1000

# tmp目录，用于保存下载下来的.crx文件
conf['tmp_path'] = './tmp/'

# 下载crx文件多线程时，指定线程数
conf['threadnum'] = 20

# 是否在解析之后删除下载的crx文件，如果以下载插件为目的可以不删除
conf['del_tmp'] = True

# 是否解析crx文件添加web_accessible_resources信息
conf['weblist'] = False

# 是否解析crx文件添加crx解压之后生成的文件名列表
conf['filelist'] = True

# 请求的UA
conf['HTTP_HEADERS'] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2403.157 Safari/537.36"
}
```

所有的config配置都可以在响应的命令行选项里进行配置。


## 关于已生成的数据文件

这里提供两个数据文件：

1. 扩展探测中用到数据文件：[用户量1000+且带有解析后处理后的web_accessible_resources的插件信息](./data/etx_weblist_info_1k.txt)
2. 包含所有扩展信息的数据文件: [所有拓展信息](./data/etx_info_all.txt)

## Example

使用20线程下载所有data/etx_info_all.txt内用户量大于10000的插件crx文件到tmp目录

`python3 geknower.py etxDownload --outfile out.txt -f data/etx_info_all.txt -t 20 -u 10000 -p /tmp `

爬取用户量大于1000000插件信息数据

`python3 geknower.py etxInfo -O out.txt -u 1000000`

## Thx

Evi1m0 Phithon

