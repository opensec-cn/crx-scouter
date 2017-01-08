from core.chromeStoreSpider import chromeStoreSpider
from core.googleExtDownloader import web_list_exec
from config import conf
import os

def conf_check():
    if not os.path.exists(conf['tmp_path']):
        exit('[!] conf tmp path not exist')

if __name__ == '__main__':
    print('[*] main start')
    conf_check()
    if 1:
        web_list_exec()
    if 0:
        csspider = chromeStoreSpider()
        csspider.run()
        csspider.get_ext_by_google()
