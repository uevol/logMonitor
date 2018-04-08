## 日志处理脚本

### Description

通过监控日志文件，对交易结果进行处理，并将处理后的结果存入MySQL，在通过grafana展现


### Requirements

    1. 须提前安装Mysql数据库

    2. 安装完成后，新建对应数据库及数据表

           # 新建数据库
               create database trade default charset=utf8;

           # 新建用户
               grant all on trade.* to admin@'%' identified by "Admin@123";

           # 新建数据表
               create table tradeRecord (tradeTime CHAR(100) NOT NULL, tradeNo CHAR(100) NOT NULL, tradeStatus CHAR(200), tradeDuration CHAR(100)) default charset=utf8;

### Usage
```
usage: monitor.py [-h] logFile db_host db_user db_pass db_name

Usage for the script

positional arguments:
  logFile     the absolute path of the log file
  db_host     the mysql server host
  db_user     the db user
  db_pass     the db password
  db_name     the db name

optional arguments:
  -h, --help  show this help message and exit
```


### Test

通过test.py脚本可进行测试，测试过程如下：

    1. 运行监控脚本，方法参考上述Usage部分说明

        python monitor.py /path/to/exampleData/test.log

    2. 运行测试脚本

        python test.py

    3. 在Mysql中(trade.tradeRecord)查看交易记录


### Log

monitor脚本运行日志存放在logMonitor.log文件中


### grafana配置

    1. 添加mysql的datasource, 用户名密码按如上配置

    2. 添加table类型的panel

    3. 编辑时选择1步骤中的datasource, 查询语句如下：
        SELECT tradeTime, tradeNo, tradeStatus, tradeDuration FROM tradeRecord ORDER BY tradeTime DESC 

### 其他说明

    1. 该脚本仅针对exampleData文件夹中的nohup.out日志格式，其他日志格式，请根据实际修改monitor.ProcessLog中的处理逻辑

    2. 如果Mysql中出现中文乱码，可以修改mysql配置文件，并重启数据库
        vi /etc/my.cnf

        ...
        [mysqld]
        character-set-server=utf8
        ...
        [client]
        default-character-set=utf8
        [mysql]
        default-character-set=utf8

