# -*- coding: utf-8 -*-
# @Author: uevol
# @Date:   2018-03-30 13:25:57
# @Last Modified by:   yangwei
# @Last Modified time: 2018-04-08 17:29:56

import os
import time

dataDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exampleData')
sampleLog = os.path.join(dataDir, 'nohup.out')
testLog = os.path.join(dataDir, 'test.log')

with open(sampleLog, 'r') as f_sampleLog:
	with open(testLog, 'a') as f_testLog:
		for line in f_sampleLog:
			print(line)
			f_testLog.write(line)