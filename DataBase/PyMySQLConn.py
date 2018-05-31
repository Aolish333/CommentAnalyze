#!/usr/bin/env python
# coding=utf-8

import pymysql
import numpy as np
import pandas as pd


def connectdb():
    print('连接到mysql服务器...')
    db = pymysql.connect("localhost","root","123456","DataDig",use_unicode=True, charset="utf8mb4")
    print('连接成功!')
    return db

def createTable(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 如果存在表先删除
    cursor.execute("DROP TABLE IF EXISTS testping")
    sql = """ CREATE  TABLE testping(
     id CHAR(10),
     name CHAR(10),
     comment VARCHAR(600)
    ) DEFAULT CHARSET=utf8mb4 auto_increment= 0 ;"""
    # 创建对应的数据库表
    print('创建数据库成功')
    cursor.execute(sql)

def insertdb(db):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()


    # 首先从文件中读取数据，然后再对数据库进行操作
    sql = 'INSERT INTO testping(id, name, comment) values(%s,%s,%s)'
    chunksize = 10 ** 1
    chunkers = pd.read_csv('H:\\CommentAnalyze\\taobao.csv', chunksize=chunksize,skiprows=0, encoding='utf-8');
    for chunker in chunkers:
        train_data = np.array(chunker)
        train_x_list = train_data.tolist()
        # print train_x_list
        # try:
            # 执行sql语句
            # cursor.execute(sql)
        cursor.executemany(sql, train_x_list)
            # 提交到数据库执行
        db.commit()
        print ('批量插入完成！')
        # except:
        #     # Rollback in case there is any error
        #     print '插入数据失败!'
        #     db.rollback()

def querydb(db):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 查询语句
    #sql = "SELECT * FROM Student \
    #    WHERE Grade > '%d'" % (80)
    sql = "SELECT * FROM testping"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            ID = row[0]
            Name = row[1]
            Commence = row[2]
            # 打印结果
            print ("ID: %s, Name: %s, Grade: %s" % \
                (ID, Name, Commence))
    except:
        print ("Error: unable to fecth data")

def deletedb(db):
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 删除语句
    sql = "DELETE FROM testping WHERE id = '%s'" % (100)

    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交修改
       db.commit()
    except:
        print ('删除数据失败!')
        # 发生错误时回滚
        db.rollback()

def closedb(db):
    db.close()

if __name__ == '__main__':
    db = connectdb()    # 连接MySQL数据库
    createTable(db)
    insertdb(db)
    querydb(db)
    db.close()