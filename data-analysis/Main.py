#!/usr/bin/env python
# coding=utf-8
import matplotlib
import wx
import pymysql
import GetDetailsById
from GetBookIds import getIds
import urllib.request
from matplotlib import pyplot


class MyEvent(wx.PyCommandEvent):  # 1 定义事件
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.eventArgs = ""

    def GetEventArgs(self):
        return self.eventArgs

    def SetEventArgs(self, args):
        self.eventArgs = args


myEVT_MY_TEST = wx.NewEventType()  # 2 创建一个事件类型
EVT_MY_TEST = wx.PyEventBinder(myEVT_MY_TEST, 1)  # 3 创建一个绑定器对象


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="京东图书爬虫程序", size=(700, 600))
        panel = wx.Panel(self, -1)

        wx.StaticText(panel, label='商品ID：', pos=(1, 10), size=(60, 25))
        self.goodsId = wx.TextCtrl(panel, pos=(65, 5), size=(100, 25))
        self.submit1 = wx.Button(panel, label='爬取', pos=(180, 5), size=(60, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit1Click, self.submit1)
        self.Bind(EVT_MY_TEST, self.OnHandle)  # 4绑定事件处理函数

        wx.StaticText(panel, label='商品ID：', pos=(270, 10), size=(60, 25))
        self.goodsId3 = wx.TextCtrl(panel, pos=(330, 5), size=(100, 25))
        self.submit3 = wx.Button(panel, label='展示', pos=(440, 5), size=(60, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit3Click, self.submit3)
        self.Bind(EVT_MY_TEST, self.OnHandle)  # 4绑定事件处理函数

        wx.StaticText(panel, label='图书种类：', pos=(1, 60), size=(60, 25))
        self.categoryId = wx.TextCtrl(panel, pos=(65, 55), size=(100, 25))

        wx.StaticText(panel, label='商品页数：', pos=(180, 60), size=(60, 25))
        self.goodsPage = wx.TextCtrl(panel, pos=(250, 55), size=(100, 25))

        wx.StaticText(panel, label='评论页数：', pos=(360, 60), size=(60, 25))
        self.speakPage = wx.TextCtrl(panel, pos=(420, 55), size=(100, 25))

        self.submit2 = wx.Button(panel, label='爬取', pos=(530, 55), size=(60, 25))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit2Click, self.submit2)
        self.Bind(EVT_MY_TEST, self.OnHandle)  # 4绑定事件处理函数

        self.contents = wx.TextCtrl(panel, pos=(5, 85), size=(700, 600), style=wx.TE_MULTILINE | wx.TE_RICH2)
        self.contents.SetInsertionPoint(0)

    def OnSubmit1Click(self, event):
        self.OnSaveSingleGoods()

    def OnSubmit2Click(self, event):
        self.OnSaveManyGoods()

    def OnSubmit3Click(self, event):
        self.OnShow()

    def OnHandle(self, event):  # 8 事件处理函数
        dlg = wx.MessageDialog(self, event.GetEventArgs(), '正在爬取...', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    # 根据id
    def OnSaveSingleGoods(self):
        evt = MyEvent(myEVT_MY_TEST, self.submit1.GetId())  # 5 创建自定义事件对象
        evt.SetEventArgs("爬取完成...")  # 6添加数据到事件

        outId, outGoodsName, outShopName, outProduceName, outISBN, outOriginPrice, outJdPrice, outjdPlusPrice = GetDetailsById.getGoodsDetailsById(
            self.goodsId.GetValue())
        comments, outCommentCount, outGoodCount, outGeneralCount, outPoorCount, outGoodRateShow, outPoorRateShow, outVideoCount, outShowCount = GetDetailsById.getCommentsByGoodsId(
            self.goodsId.GetValue(), 1)

        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='my-crawler',
            charset='utf8'
        )
        # 获取游标
        cursor = conn.cursor()
        # 执行sql语句
        sql1 = "INSERT INTO goods(goodsId,goodsName,shopName,goodsProduce,ISBN,originPrice,jdPrice,jdPlusPrice,commentCount,goodCount,generalCount,poorCount,videoCount,showCount,poorRateShow,goodRateShow) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 返回结果是受影响的行数
        rows = cursor.execute(sql1, (outId, outGoodsName, outShopName, outProduceName, outISBN, outOriginPrice,
                                     outJdPrice,
                                     outjdPlusPrice, outCommentCount, outGoodCount, outGeneralCount, outPoorCount,
                                     outVideoCount, outShowCount, outPoorRateShow, outGoodRateShow))

        sql2 = "INSERT INTO comment(goodsId,comment,creationTime) VALUES(%s,%s,%s)"
        params = []
        for item in comments[1:]:
            content = item['content']
            creationTime = item['creationTime']
            params.append((outId, content, creationTime))
        cursor.executemany(sql2, params)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        self.contents.SetLabel("商品ID： " + str(outId) +
                               "\n商品名： " + str(outGoodsName) +
                               "\n店铺名称： " + str(outShopName) +
                               "\n出版社： " + str(outProduceName) +
                               "\nISBN： " + str(outISBN) +
                               "\n定价： " + str(outOriginPrice) +
                               "\n京东价： " + str(outJdPrice) +
                               "\n京东PLUS会员价： " + str(outjdPlusPrice) +
                               "\n全部评论总数： " + str(outCommentCount) +
                               "\n好评数量： " + str(outGoodCount) +
                               "\n中评数量： " + str(outGeneralCount) +
                               "\n差评数量： " + str(outPoorCount) +
                               "\n好评度： " + str(outGoodRateShow) + "%" +
                               "\n差评度： " + str(outPoorRateShow) + "%" +
                               "\n视频晒单数量： " + str(outVideoCount) +
                               "\n晒图数量： " + str(outShowCount) +
                               "\n-------------------------------------------------------"
                               )
        self.GetEventHandler().ProcessEvent(evt)  # 7 处理事件

    # 同类书籍
    def OnSaveManyGoods(self):
        evt = MyEvent(myEVT_MY_TEST, self.submit2.GetId())  # 5 创建自定义事件对象
        evt.SetEventArgs("爬取完成...")  # 6添加数据到事件
        id_list = 0
        keyword = urllib.request.quote(self.categoryId.GetValue())
        for pagenum in range(0, int(self.goodsPage.GetValue())):
            url = "https://search.jd.com/Search?keyword=" + keyword + "&enc=utf-8&page=" + str(
                pagenum + 2)
            # print("正在爬取第" + str(pagenum + 1) + "页数据！！！")
            id_list = getIds(url)

        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='my-crawler',
            charset='utf8'
        )
        # 获取游标
        cursor = conn.cursor()

        for myId in id_list:
            print(myId)
            outId, outGoodsName, outShopName, outProduceName, outISBN, outOriginPrice, outJdPrice, outjdPlusPrice = GetDetailsById.getGoodsDetailsById(
                myId)
            comments, outCommentCount, outGoodCount, outGeneralCount, outPoorCount, outGoodRateShow, outPoorRateShow, outVideoCount, outShowCount = GetDetailsById.getCommentsByGoodsId(
                myId, 1)
            self.contents.AppendText("图书ID： " + str(outId) +
                                     "\n图书名称： " + str(outGoodsName) +
                                     "\n店铺名称： " + str(outShopName) +
                                     "\n出版社： " + str(outProduceName) +
                                     "\nISBN： " + str(outISBN) +
                                     "\n定价： " + str(outOriginPrice) +
                                     "\n京东价： " + str(outJdPrice) +
                                     "\n京东PLUS会员价： " + str(outjdPlusPrice) +
                                     "\n全部评论总数： " + str(outCommentCount) +
                                     "\n好评数量： " + str(outGoodCount) +
                                     "\n中评数量： " + str(outGeneralCount) +
                                     "\n差评数量： " + str(outPoorCount) +
                                     "\n好评度： " + str(outGoodRateShow) + "%" +
                                     "\n差评度： " + str(outPoorRateShow) + "%" +
                                     "\n视频晒单数量： " + str(outVideoCount) +
                                     "\n晒图数量： " + str(outShowCount) +
                                     "\n-------------------------------------------------------"
                                     )
            # 执行sql语句
            sql1 = "INSERT INTO goods(goodsId,goodsName,shopName,goodsProduce,ISBN,originPrice,jdPrice,jdPlusPrice,commentCount,goodCount,generalCount,poorCount,videoCount,showCount,poorRateShow,goodRateShow) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 返回结果是受影响的行数
            rows = cursor.execute(sql1, (outId, outGoodsName, outShopName, outProduceName, outISBN, outOriginPrice,
                                         outJdPrice,
                                         outjdPlusPrice, outCommentCount, outGoodCount, outGeneralCount, outPoorCount,
                                         outVideoCount, outShowCount, outPoorRateShow, outGoodRateShow))

            sql2 = "INSERT INTO comment(goodsId,comment,creationTime) VALUES(%s,%s,%s)"
            params = []
            for item in comments[1:]:
                content = item['content']
                creationTime = item['creationTime']
                params.append((outId, content, creationTime))
            cursor.executemany(sql2, params)
        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()
        self.GetEventHandler().ProcessEvent(evt)  # 7 处理事件

    # 根据id show
    def OnShow(self):
        evt = MyEvent(myEVT_MY_TEST, self.submit3.GetId())  # 5 创建自定义事件对象
        evt.SetEventArgs("根据商品Id=" + self.goodsId3.GetValue() + "展示")  # 6添加数据到事件
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='my-crawler',
            charset='utf8',
        )
        # 获取游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行sql语句
        sql1 = "SELECT DATE_FORMAT(creationTime,'%Y%m') months ,COUNT(id) as num FROM comment WHERE goodsId = " + str(
            self.goodsId3.GetValue()) + " GROUP BY months"
        sql2 = "SELECT * FROM goods WHERE goodsId = " + str(self.goodsId3.GetValue())
        cursor.execute(sql1)
        res1 = cursor.fetchall()
        cursor.execute(sql2)
        res2 = cursor.fetchall()
        json2 = res2[0]
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()

        # 柱状图
        x1 = []
        y1 = []
        for item in res1:
            x1.append(item['months'])
            y1.append(item['num'])
        matplotlib.rcParams['font.family'] = 'SimHei'
        pyplot.title("历史评论柱状图")
        pyplot.bar(x1, y1)
        pyplot.show()
        # 折线图
        x2 = ["好评数", "中评数", "差评数", "视频数", "晒图数"]
        y2 = [json2['goodCount'], json2['generalCount'], json2['poorCount'], json2['videoCount'], json2['showCount']]
        # 生成图表
        matplotlib.rcParams['font.family'] = 'SimHei'
        pyplot.plot(x2, y2)
        # 设置横坐标为year，纵坐标为population，标题为Population year correspondence
        pyplot.xlabel("评价")
        pyplot.ylabel("数量")
        pyplot.title("根据评论展示月销量")
        # 设置纵坐标刻度
        # pyplot.yticks([0, 25, 50, 75, 90])
        # 设置填充选项：参数分别对应横坐标，纵坐标，纵坐标填充起始值，填充颜色（可以有更多选项）
        # pyplot.fill_between(month, number, 10, color='green')
        pyplot.fill_between(x2, y2)
        # 显示图表
        pyplot.show()
        self.GetEventHandler().ProcessEvent(evt)  # 7 处理事件


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show(True)
    app.MainLoop()
