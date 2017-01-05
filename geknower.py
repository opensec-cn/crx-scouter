from core.chromeStoreSpider import chromeStoreSpider
from core.googleExtDownloader import web_list_exec

if __name__ == '__main__':
    print('[*] main start')
    if True:
        web_list_exec()
    if False:
        csspider = chromeStoreSpider()
        csspider.run()
