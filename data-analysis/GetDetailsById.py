# -*- coding: UTF-8 -*-
import urllib.request
from lxml import etree
import json

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'uuid_tt_dd=10_35489889920-1563497330616-876822; ...... ',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}


def getHeaders(productid):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'uuid_tt_dd=10_35489889920-1563497330616-876822; ...... ',
        "Referer": "https://item.jd.com/%s.html" % (productid),
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    return header


def getGoodsDetailsById(goodsId):
    url = "http://item.jd.com/" + goodsId + ".html"
    urlPrice = "https://p.3.cn/prices/get?skuId=" + goodsId
    # 商品名称
    req1 = urllib.request.Request(url=url, headers=header)
    data1 = urllib.request.urlopen(req1).read().decode("utf-8", "ignore")
    goodsHtml = etree.HTML(data1)
    goodsName = goodsHtml.xpath('/html/head/title')
    goodsShop = goodsHtml.xpath('//ul[@id="parameter2"]/li')
    # 商品价格
    req2 = urllib.request.Request(url=urlPrice, headers=getHeaders(goodsId))
    data2 = urllib.request.urlopen(req2).read().decode("utf-8", "ignore")
    data2 = str(data2).replace('[', '').replace(']', '')
    goodsPrice = json.loads(data2)
    outId = goodsId
    outGoodsName = goodsName[0].text
    outShopName = goodsShop[0].attrib.get('title')
    outProduceName = goodsShop[1].attrib.get('title')
    outISBN = goodsShop[2].attrib.get('title')
    outOriginPrice = float(goodsPrice["m"])
    outJdPrice = goodsPrice["p"]
    outjdPlusPrice = goodsPrice["p"]
    if ("tpp" in goodsPrice):
        outjdPlusPrice = goodsPrice["tpp"]
        # print("京东plus价格： " + goodsPrice["tpp"])
    # 输出
    # print("商品ID： " + outId)
    # print("商品名： " + outGoodsName)
    # print("店铺名称： " + outShopName)
    # print("出版社： " + outProduceName)
    # print("ISBN： " + outISBN)
    # print("定价： " + outOriginPrice)
    # print("京东价： " + outJdPrice)
    # print("京东PLUS会员价" + outjdPlusPrice)
    return outId, outGoodsName, outShopName, outProduceName, outISBN, outOriginPrice, outJdPrice, outjdPlusPrice


def getCommentsByGoodsId(goodsId, commentPage):
    urlSpeak = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=" + goodsId + "&score=0&sortType=5&page=" + str(
        commentPage) + "&pageSize=10&isShadowSku=0&fold=1"
    # 评论
    req3 = urllib.request.Request(url=urlSpeak, headers=getHeaders(id))
    data3 = urllib.request.urlopen(req3).read().decode("gbk", "ignore")
    data3 = str(data3).replace('fetchJSON_comment98(', '').replace(');', '')
    goodsSpeak = json.loads(data3)
    productCommentSummary = goodsSpeak["productCommentSummary"]
    comments = goodsSpeak["comments"]
    outCommentCount = productCommentSummary["commentCount"]
    outGoodCount = productCommentSummary["goodCount"]
    outGeneralCount = productCommentSummary["generalCount"]
    outPoorCount = productCommentSummary["poorCount"]
    outGoodRateShow = productCommentSummary["goodRateShow"]
    outPoorRateShow = productCommentSummary["poorRateShow"]
    outVideoCount = productCommentSummary["videoCount"]
    outShowCount = productCommentSummary["showCount"]
    # print("全部评论总数： " + str(outCommentCount))
    # print("好评数量： " + str(outGoodCount))
    # print("中评数量： " + str(outGeneralCount))
    # print("差评数量： " + str(outPoorCount))
    # print("好评度： " + str(outGoodRateShow) + "%")
    # print("差评度： " + str(outPoorRateShow) + "%")
    # print("视频晒单： " + str(outVideoCount))
    # print("晒图： " + str(outShowCount))
    # print("-------------------------------------------评论-------------------------------------------")
    # for item in comments[1:]:
    #     content = item['content']
    #     print(content)
    # print("-------------------------------------------评论-------------------------------------------")
    return comments, outCommentCount, outGoodCount, outGeneralCount, outPoorCount, outGoodRateShow, outPoorRateShow, outVideoCount, outShowCount


if __name__ == '__main__':
    getGoodsDetailsById(id)
    getCommentsByGoodsId(id, 1)
