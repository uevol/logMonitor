# -*- coding: utf-8 -*-
# @Author: yangwei
# @Date:   2018-03-27 14:22:43
# @Last Modified by:   uevol
# @Last Modified time: 2018-03-30 14:53:29

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


def ProcessLog(myTailer, mongoConnect):
    try:
        for line in myTailer.follow:
            if 'tradeFinish:' in line:
                print(line)
                arr = line.split('tradeFinish:')
                tradeTime = arr[0].split(' TRACE')[0]
                arr1 = arr[1].split('：')
                tradeNo = arr1[1]
                tradeStatus = ': '.join(arr1[2:-2])
                tradeDuration = arr1[-1]
                tradeInfo = {'tradeTime': tradeTime, 'tradeNo': tradeNo, 'tradeStatus': tradeStatus, 'tradeDuration': tradeDuration}
                mongoConnect.mongo.trade.tradeRecord.insert_one(tradeInfo)
    except Exception as e:
        logger.error(str(e))



if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Usage for the script")
        parser.add_argument('logFile', type=str, help='the absolute path of the log file')
        parser.add_argument('--mongoHost', type=str, help='the mongodb host')
        parser.add_argument('--mongoPort', type=str, help='the mongodb port')
        parser.add_argument('--mongoUser', type=str, help='the mongodb user')
        parser.add_argument('--mongoPass', type=str, help='the mongodb password')
        args = parser.parse_args()
        
        myTailer = MyTailer(args.logFile)
        mongoConnect = MongoConnect(args.mongoHost, args.mongoPort, args.mongoUser, args.mongoPass)
        ProcessLog(myTailer, mongoConnect)
    except Exception as e:
        raise e

























