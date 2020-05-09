# -*- coding: UTF-8 -*-
import urllib.request
import re

# keyname = "图书"  # 搜索的图书类型
# page = 3
# key = urllib.request.quote(keyname)  # 关键词转换为URL编码
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'uuid_tt_dd=10_35489889920-1563497330616-876822; ...... ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


def getIds(url):
    req = urllib.request.Request(url=url, headers=header)
    data = urllib.request.urlopen(req).read().decode("utf-8", "ignore")
    id_pat = '<strong class="J_(.*?)" '
    id_list = re.compile(id_pat).findall(data)
    return id_list


# if __name__ == '__main__':
#     for pagenum in range(0, page):
#         url = "https://search.jd.com/Search?keyword=" + key + "&enc=utf-8&page=" + str(pagenum + 2)
#         print("正在爬取第" + str(pagenum + 1) + "页数据！！！")
#         id_list = getIds(url)
