import os
import json
import time
import shutil
import requests
import zipfile
import io
from lib.common import dict2file
from lib.threadManager import ThreadPool
from config import conf
from lib.common import Error
from lib.common import do_ten_times_til_true

ext_download_url_base = 'https://clients2.google.com/service/update2/crx?' \
    + 'response=redirect&prodversion=49.0&x=id%3D{id}%26installsource%3Dondemand%26uc'


@do_ten_times_til_true
def download_ext(extid='', filepath=''):
    url = ext_download_url_base.format(id=extid)
    res = requests.get(url, verify=False, stream=True,\
            allow_redirects=True, timeout=10, headers=conf['HTTP_HEADERS'])
    if res.status_code != 200:
        raise requests.RequestException(u"Status code error: {}".format(res.status_code))
    with io.open(filepath, 'wb', encoding='utf-8') as f:
        for chunk in res.iter_content(chunk_size=512 * 1024): 
            if chunk: 
                f.write(chunk)
    return True


def web_list_exec():
    print('[*] -- web list exec ---')
    count = 0
    pool = ThreadPool(conf['threadnum'])
    # import pdb;pdb.set_trace()
    with io.open(conf['data_file'], 'r', encoding='utf-8') as f:
        for count, line in enumerate(f):
            info = json.loads(line.strip())
            pool.add_task(ext_info_add_list, extinfo=info)
    pool.destroy()
    count = count + 1
    for i in range(count):
        result = pool.get_task()
        if result:
            dict2file(result, conf['etx_info_weblist_file'])


def unzip_ext(extpath='', extid=''):
    extpath = os.path.realpath(extpath)
    zip_ref = zipfile.ZipFile(extpath, 'r')
    zip_ref.extractall(os.path.join(os.path.dirname(extpath), extid))
    zip_ref.close()


def manifestfile_to_weblist(file=''):
    with io.open(file, 'r', encoding='utf-8') as f:
        info = json.load(f)
        web_list = info.get('web_accessible_resources')
        return web_list


def ext_info_add_list(extinfo = {}):
    extid = extinfo.get('id')
    print('[*] id : ' + extid)
    # import pdb;pdb.set_trace()
    path = conf['tmp_path']
    if extid:
        filepath = os.path.join(path, extid + '.crx')
        flag = download_ext(extid, filepath)
        if flag:
            unzip_ext(extpath=filepath, extid=extid)
            manifest_file = os.path.join(path, extid, 'manifest.json')
            web_list = manifestfile_to_weblist(manifest_file)
            try:
                os.remove(filepath)
                shutil.rmtree(os.path.join(path, extid))
            except FileNotFoundError as e:
                print(str(e))
            if web_list:
                extinfo['web_accessible_resources'] = web_list
                return extinfo
