# -*- coding: UTF-8 -*-
import pymysql


# 建立数据库连接
def save():
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
    sql = "INSERT INTO goods(goodsName,shopName,goodsProduce,ISBN,originPrice,jdPrice,jdPlusPrice,commentCount,goodCount,generalCount,poorCount,videoCount,showCount,poorRateShow,goodRateShow) VALUES(%s,%s,%s,%s,%f,%f,%f,%d,%d,%d,%d,%d,%d,%d,%d,%d)"
    rows = cursor.execute(sql,)  # 返回结果是受影响的行数
    print(cursor.fetchone())
    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()
