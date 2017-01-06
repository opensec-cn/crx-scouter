from core.chromeStoreSpider import chromeStoreSpider
from core.googleExtDownloader import web_list_exec

if __name__ == '__main__':
    print('[*] main start')
    if False:
        web_list_exec()
    if True:
        csspider = chromeStoreSpider()
        # csspider.run()
        csspider.get_ext_by_google()
