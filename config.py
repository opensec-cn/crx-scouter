# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

conf = {}


# 保存插件信息的文件，文件格式是每一行一个json，存储一个插件信息
conf['data_file'] = './data/data.json'

# 生成添加web_accessible_resources或者文件名列表所保存的json，这个生成会根据conf['data_file']内的插件信息进行生成
conf['etx_info_weblist_file'] = './data/data_weblist.json'

# 用户数限制，爬取数据时只爬取用户量多余该数的插件信息
conf['more_then_user_num'] = 1000

# tmp目录，用于保存下载下来的.crx文件
conf['tmp_path'] = './tmp/'

# 下载crx文件多线程时，指定线程数
conf['threadnum'] = 20

# 是否在解析之后删除下载的crx文件，如果以下载插件为目的可以不删除
conf['del_tmp'] = False

# 是否解析crx文件添加web_accessible_resources信息
conf['weblist'] = False

# 是否解析crx文件添加crx解压之后生成的文件名列表
conf['filelist'] = False

# 请求的UA
conf['HTTP_HEADERS'] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2403.157 Safari/537.36"
}

