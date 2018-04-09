# -*- coding: utf-8 -*-
# @Author: yangwei
# @Date:   2018-03-27 14:22:43
# @Last Modified by:   uevol
# @Last Modified time: 2018-04-09 10:58:22

import os
import sys
import tailer

import logging
import argparse

from pymongo import MongoClient
try:
    from urllib import quote_plus
except ImportError:
    # For Python 3
    from urllib.parse import quote_plus

import MySQLdb

logger = logging.getLogger('logMonitor')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

fileHandler = logging.FileHandler('logMonitor.log')
fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.setLevel(logging.ERROR)


class MyTailer(object):
    """docstring for mytailer"""
    def __init__(self, file):
        super(MyTailer, self).__init__()
        self.__file = file

    @property
    def tail(self, n):
        return tailer.tail(open(self.__file), n)

    @property
    def head(self, n):
        return tailer.tail(open(self.__file), n)

    @property
    def follow(self):
        return tailer.follow(open(self.__file))

class MongoConnect(object):
    """docstring for M"""
    def __init__(self, host, port, user, passwd):
        super(MongoConnect, self).__init__()
        self.__host = host or 'localhost'
        self.__port = port or 27017
        self.__user = user
        self.__passwd = passwd

    @property
    def mongo(self):
        try:
            if self.__user and self.__passwd:
               MONGO_USER, MONGO_PASS = quote_plus(self.__user), quote_plus(self.__passwd)
               mongo = MongoClient('mongodb://%s:%s@%s:%s' % (self.__host, self.__port, MONGO_USER, MONGO_PASS))
            else:
               mongo = MongoClient(self.__host, self.__port)
        except Exception as e:
            raise e
        return mongo


class MySQL(object):
    """docstring for MySQL"""
    def __init__(self, db_host, db_user, db_pass, db_name):
        super(MySQL, self).__init__()
        self.__db = MySQLdb.connect(db_host, db_user, db_pass, db_name, charset='utf8')
        self.__cursor = self.__db.cursor()


    def execute(self, sql, params):
        try:
            self.__cursor.execute(sql, params)
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            logger.error(str(e))
        # finally:
        #     self.__db.close()

def ProcessLog(myTailer, connect):
    try:
        for line in myTailer.follow:
            if 'GH_MPMS_MONITOR' in line:
                arr = line.split(' - ')
                tradeTime = arr[0].split('[INFO ]')[0].strip('[]')
                arr1 = arr[1].split('#')
                tradeNo = arr1[0]
                tradeDuration = arr1[-1].split('：[')[-1][:-4]
                # tradeInfo = {'tradeTime': tradeTime, 'tradeNo': tradeNo, 'tradeStatus': tradeStatus, 'tradeDuration': tradeDuration}
                # connect.mongo.trade.tradeRecord.insert_one(tradeInfo)
                sql = "INSERT INTO tradeRecord (tradeTime, tradeNo, tradeDuration)\
                 VALUES (%s, %s, %s, %s)"
                connect.execute(sql, (tradeTime.decode('utf-8'), tradeNo.decode('utf-8'), tradeDuration.decode('utf-8')))
    except Exception as e:
        logger.error(str(e))



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Usage for the script")
        parser.add_argument('logFile', type=str, help='the absolute path of the log file')

        ## for mongodb
        # parser.add_argument('--mongoHost', type=str, help='the mongodb host')
        # parser.add_argument('--mongoPort', type=str, help='the mongodb port')
        # parser.add_argument('--mongoUser', type=str, help='the mongodb user')
        # parser.add_argument('--mongoPass', type=str, help='the mongodb password')
        # args = parser.parse_args()
        # connect = MongoConnect(args.mongoHost, args.mongoPort, args.mongoUser, args.mongoPass)
        # ProcessLog(myTailer, connect)

        ## for mysql
        parser.add_argument('db_host', type=str, help='the mysql server host')
        parser.add_argument('db_user', type=str, help='the db user')
        parser.add_argument('db_pass', type=str, help='the db password')
        parser.add_argument('db_name', type=str, help='the db name')
        args = parser.parse_args()
        connect = MySQL(args.db_host, args.db_user, args.db_pass, args.db_name)

        myTailer = MyTailer(args.logFile)
        ProcessLog(myTailer, connect)
    except Exception as e:
        raise e

























