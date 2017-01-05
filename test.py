import requests
import json
from config import conf

flag = True

ext_item_url = '''https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=CN&pv=20161108&mce=atf%2Ceed%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Ceuf%2Cmac%2Cfcf%2Crma%2Cpot%2Cevt%2Cigb&requestedCounts=infiniteWall%3A{limit}%3A0%3Afalse&token=featured%3A0%4010316222%3A7%3Afalse%2Cmcol%23top_picks_productivity%3A0%4010316223%3A11%3Atrue%2CinfiniteWall%3A0%4010316253%3A{start}%3Afalse&category={category}&_reqid=3058318&rt=j'''

def get_blogging_count():
    start = 866
    count = 0
    ext_item_url = '''https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=CN&pv=20161108&mce=atf%2Ceed%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Ceuf%2Cmac%2Cfcf%2Crma%2Cpot%2Cevt%2Cigb&requestedCounts=infiniteWall%3A{limit}%3A0%3Afalse&token=featured%3A0%4010316222%3A7%3Afalse%2Cmcol%23top_picks_productivity%3A0%4010316223%3A11%3Atrue%2CinfiniteWall%3A0%4010316253%3A{start}%3Afalse&category={category}&_reqid=3058318&rt=j'''
    while flag:
        start = start + 1
        category = 'ext/10-blogging'
        url = ext_item_url.format(limit=1, start=str(start), category='ext/10-blogging')
        try:
            response = requests.post(url, verify=False,\
                    allow_redirects=False, timeout=10, headers=conf['HTTP_HEADERS'])
            import ipdb;ipdb.set_trace()
            res = response.text
            if response.status_code != 200:
                raise requests.RequestException(u"Status code error: {}".format(response.status_code))
        except requests.RequestException as e:
            print(str(e))
            continue

        if res:
            count = count + 1
            # import pdb;pdb.set_trace()
            json_list = json.loads(res.lstrip(")]}'\n"))
            name = json_list[0][1][1][0][1]
            print(start)
            print(name)


def get_ext_name(limit=0, start=0):
    url = ext_item_url.format(limit=str(limit), start=str(start), category='ext/10-blogging')
    try:
        response = requests.post(url, verify=False,\
                allow_redirects=False, timeout=10, headers=conf['HTTP_HEADERS'])
        import pdb;pdb.set_trace()
        res = response.text
        if response.status_code != 200:
            raise requests.RequestException(u"Status code error: {}".format(response.status_code))
    except requests.RequestException as e:
        print(str(e))

    if res:
        json_list = json.loads(res.lstrip(")]}'\n"))
        name = json_list[0][1][1][0][1]
        print(start)
        print(name)


if __name__ == '__main__':
    get_blogging_count()
