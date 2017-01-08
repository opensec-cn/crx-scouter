import json
import requests
from config import conf
from lib.common import get_int, dict2file, do_ten_times_til_true

class chromeStoreSpider(object):
    """获取Chrome WebStore中所有的拓展信息"""

    ext_item_url = '''https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=CN&pv=20161108&mce=atf%2Ceed%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Ceuf%2Cmac%2Cfcf%2Crma%2Cpot%2Cevt%2Cigb&requestedCounts=infiniteWall%3A{limit}%3A0%3Afalse&token=featured%3A0%4010316222%3A7%3Afalse%2Cmcol%23top_picks_productivity%3A0%4010316223%3A11%3Atrue%2CinfiniteWall%3A0%4010316253%3A{start}%3Afalse&category={category}&_reqid=3058318&rt=j'''

    def __init__(self):
        super(chromeStoreSpider, self).__init__()
        self.limit = 200
        self.start = 1
        self.category_list = [
            'ext/10-blogging',
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
        ]
        self.json_path = conf['data_file']
    
    def run(self):
        for category in self.category_list:
            print('[*] category : ' + str(category))
            start = self.start
            while True:
                print('[*] start : %s !!!!'%str(start))
                url = self.ext_item_url.format(limit=self.limit, start=start, category=category)
                # import pdb;pdb.set_trace()
                res = self.get_ext_item_reps(url)
                jsonlist = self._res_to_info_list(res)
                if jsonlist:
                    for json in jsonlist:
                        id_str, users, info = self._list2info(json)
                        if users >= conf['more_then_user_num']:
                            print('[*] id : %s'%id_str)
                            dict2file(info, path=self.json_path)
                else:
                    break
                start = start + self.limit


    def _list2info(self, list):
        if list:
            try:
                id_str = list[0]
                users = get_int(str(list[23]))
                info = {
                    "id" : id_str,
                    "name" : list[1],
                    "stars" : list[22],
                    "users" : list[23],
                    "category" : list[9],
                    "url" : list[37]
                }
                return (id_str, users, info)
            except IndexError as e:
                # raise e
                # import pdb;pdb.set_trace()
                pass

    @do_ten_times_til_true
    def get_ext_item_reps(self, url):
        # 尝试请求十次防止请求失败，数据丢失。
        try:
            response = requests.post(url, verify=False,\
                    allow_redirects=False, timeout=10, headers=conf['HTTP_HEADERS'])
            res = response.text
            if response.status_code != 200:
                raise requests.RequestException(u"Status code error: {}".format(response.status_code))
            if response.status_code == 200:
                return res
        except requests.RequestException as e:
            return False

    def get_ext_by_google(self):
        url = "https://chrome.google.com/webstore/ajax/item?pv=20161108&count=209&category=ext/15-by-google"
        res = self.get_ext_item_reps(url)
        jsonlist = json.loads(res.lstrip(")]}'\n"))
        jsonlist = jsonlist[1][1]
        if jsonlist:
            for json_ in jsonlist:
                id_str, users, info = self._list2info(json_)
                if users >= conf['more_then_user_num']:
                    print('[*] id : %s'%id_str)
                    dict2file(info, path=self.json_path)

    def _res_to_info_list(self, res=''):
        if res:
            infojson = json.loads(res.lstrip(")]}'\n"))
            return infojson[0][1][1]
        else: 
            # import pdb;pdb.set_trace()
            # raise Exception() 
            pass


