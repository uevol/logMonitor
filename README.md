## 日志处理脚本

### Description

通过监控日志文件，对交易结果进行处理，并将处理后的结果存入mongodb

### Usage
```
usage: monitor.py [-h] [--mongoHost MONGOHOST] [--mongoPort MONGOPORT]
                  [--mongoUser MONGOUSER] [--mongoPass MONGOPASS]
                  logFile

Usage for the script

positional arguments:
  logFile               the absolute path of the log file

optional arguments:
  -h, --help            show this help message and exit
  --mongoHost MONGOHOST
                        the mongodb host
  --mongoPort MONGOPORT
                        the mongodb port
  --mongoUser MONGOUSER
                        the mongodb user
  --mongoPass MONGOPASS
                        the mongodb password
```

### Test

通过test.py脚本可进行测试，测试过程如下：

    1. 运行监控脚本，方法参考上述Usage部分说明

    python monitor.py /path/to/exampleData/test.log

    2. 运行测试脚本

    python test.py

    3. 在mongodb中查看交易记录


### Log

monitor脚本运行日志存放在logMonitor.log文件中


### 其他说明

    1. 请自行提前安装mongodb数据库

    2. 该脚本仅针对exampleData文件夹中的nohup.out日志格式，其他日志格式，请根据实际修改monitor.ProcessLog中的处理逻辑



