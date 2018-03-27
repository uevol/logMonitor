# -*- coding: utf-8 -*-
# @Author: yangwei
# @Date:   2018-03-27 14:22:43
# @Last Modified by:   uevol
# @Last Modified time: 2018-03-27 15:47:47

import os
import sys
import tailer

from pymongo import MongoClient
try:
    from urllib import quote_plus
except ImportError:
    # For Python 3
    from urllib.parse import quote_plus

class MyTailer(object):
    """docstring for mytailer"""
    def __init__(self, file):
        super(MyTailer, self).__init__()
        self.file = file

    @property
    def tail(self, n):
        return tailer.tail(open(self.file), n)

    @property
    def head(self, n):
        return tailer.tail(open(self.file), n)

    @property
    def follow(self):
        return tailer.follow(open(self.file))

class MongoConnect(object):
    """docstring for M"""
    def __init__(self, host='localhost', port=27017, user=None, passwd=None):
        super(MongoConnect, self).__init__()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    @property
    def mongo(self):
        if self.user and self.passwd:
           MONGO_USER, MONGO_PASS = quote_plus(self.user), quote_plus(self.passwd)
           mongo = MongoClient('mongodb://%s:%s@%s:%s' % (self.host, self.port, MONGO_USER, MONGO_PASS))
        else:
           mongo = MongoClient(self.host, self.port)
        return mongo


def ProcessLog(follower):
    Mconnect = MongoConnect()
    for line in follower:
        if 'tradeFinish:' in line:
            arr = line.split('tradeFinish:')
            tradeTime = arr[0].split(' TRACE')[0]
            arr1 = arr[1].split('：')
            tradeNo = arr1[1]
            tradeStatus = ': '.join(arr1[2:-2])
            tradeDuration = arr1[-1]
            tradeInfo = {'tradeTime': tradeTime, 'tradeNo': tradeNo, 'tradeStatus': tradeStatus, 'tradeDuration': tradeDuration}
            # print(tradeInfo)
            Mconnect.mongo.trade.tradeRecord.insert_one(tradeInfo)
        else:
            pass

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file = sys.argv[1]
    else:
        print('user example log for testing')
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example_log', 'nohup.out')
    mytailer = MyTailer(file)
    ProcessLog(mytailer.follow)
























