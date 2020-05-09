# -*- coding: UTF-8 -*-
import wx

app = wx.App()
win = wx.Frame(None, title="京东图书爬虫程序", size=(700, 600))
win.Show()

wx.StaticText(win, label='商品ID：', pos=(1, 10), size=(60, 25))
goodsId = wx.TextCtrl(win, pos=(65, 5), size=(100, 25))
submit1 = wx.Button(win, label='爬取', pos=(180, 5), size=(60, 25))

wx.StaticText(win, label='商品种类：', pos=(1, 60), size=(60, 25))
categoryId = wx.TextCtrl(win, pos=(65, 55), size=(100, 25))

wx.StaticText(win, label='商品页数：', pos=(180, 60), size=(60, 25))
goodsPage = wx.TextCtrl(win, pos=(250, 55), size=(100, 25))

wx.StaticText(win, label='评论页数：', pos=(360, 60), size=(60, 25))
speakPage = wx.TextCtrl(win, pos=(420, 55), size=(100, 25))

submit2 = wx.Button(win, label='爬取', pos=(530, 55), size=(60, 25))

contents = wx.TextCtrl(win, pos=(5, 85), size=(700, 600), style=wx.TE_MULTILINE | wx.HSCROLL)

app.MainLoop()
