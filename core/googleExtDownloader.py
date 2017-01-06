import os
import json
import time
import shutil
import requests
import zipfile
import codecs
import fnmatch
import io
from config import conf
from lib.common import dict2file
from lib.threadManager import ThreadPool
from lib.common import Error
from lib.common import do_ten_times_til_true, lstrip_bom

ext_download_url_base = 'https://clients2.google.com/service/update2/crx?' \
    + 'response=redirect&prodversion=49.0&x=id%3D{id}%26installsource%3Dondemand%26uc'


@do_ten_times_til_true
def download_ext(extid='', filepath=''):
    url = ext_download_url_base.format(id=extid)
    res = requests.get(url, verify=False, stream=True,\
            allow_redirects=True, timeout=10, headers=conf['HTTP_HEADERS'])
    if res.status_code != 200:
        raise requests.RequestException(u"Status code error: {}".format(res.status_code))
    with io.open(filepath, 'wb') as f:
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


def wildcard_char_done(etxfile='', weblist=[]):
    wildcard_filename_list = is_wildcard_char(weblist)
    if wildcard_filename_list:
        for wildcard_filename in wildcard_filename_list:
            wildcard_filename = wildcard_filename.rstrip('/')
            if wildcard_filename != "*":
               zipf = zipfile.ZipFile(etxfile, 'r')
               filenamelist = zipf.namelist()
               zipf.close()
               for name in filenamelist:
                    name = name.rstrip('/')
                   if not name.endswith('/') and fnmatch.fnmatch(name, wildcard_filename):
                       return [name]
    return weblist


def is_wildcard_char(weblist=[]):
    for webfile in weblist:
        if '*' in webfile:
            return weblist


def unzip_ext(extpath='', extid=''):
    try:
        extpath = os.path.realpath(extpath)
        zip_ref = zipfile.ZipFile(extpath, 'r')
        zip_ref.extract('manifest.json', os.path.join(os.path.dirname(extpath), extid))
        zip_ref.close()
    except UnicodeEncodeError as e:
        print(str(e))
        print('[!] UnicodeEncodeError in id:{}'.format(str(extid)))


def manifestfile_to_weblist(file=''):
    with codecs.open(file, 'r', encoding='utf-8-sig') as f:
        try:
            info = json.loads(f.read())
            web_list = info.get('web_accessible_resources')
            return web_list
        except ValueError as e:
            print(str(e))
            print('[!] ValueError when manifestfile_to_weblist in :{}'.format(file))


def ext_info_add_list(extinfo = {}):
    extid = extinfo.get('id')
    print('[*] id : ' + extid)
    path = conf['tmp_path']
    if extid:
        filepath = os.path.join(path, extid + '.crx')
        flag = download_ext(extid, filepath)
        if flag:
            unzip_ext(extpath=filepath, extid=str(extid))
            manifest_file = os.path.join(path, extid, 'manifest.json')
            web_list = manifestfile_to_weblist(manifest_file)
            if web_list:
                web_list = wildcard_char_done(etxfile=filepath, weblist=web_list)
            try:
                os.remove(filepath)
                # shutil.rmtree(os.path.join(path, extid))
            except FileNotFoundError as e:
                print(str(e))
            if web_list:
                extinfo['web_accessible_resources'] = web_list
                return extinfo
