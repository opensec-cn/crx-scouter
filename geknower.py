from core.chromeStoreSpider import chromeStoreSpider
from core.googleExtDownloader import web_list_exec

if __name__ == '__main__':
    print('[*] main start')
    if 1:
        web_list_exec()
    if 0:
        csspider = chromeStoreSpider()
        csspider.run()
        csspider.get_ext_by_google()
