# 在 Linux 系统实现自动上报

功能原理：使用`Cron`软件实现定时启动

## 下载程序&配置运行环境

### 安装Python3&pip3&Git

#### CentOS

`yum install python3 python3-pip git`

#### Ubuntu/Debian

`apt install python3 python3-pip git` 

### 下载代码并配置依赖环境

注：以`/usr/local/src`为工作目录的上层目录

```
cd /usr/local/src
git clone https://github.com/imldy/Health-Data-Post.git
cd Health-Data-Post # 进入工作目录
pip3 install urllib3 lxml requests
# 自行修改好 students_data.json
python3 HealthDataPost.py # 测试运行
```

## 设置自动启动

`crontab` 命令用于维护每个用户的任务时间表（crontab）文件

执行`crontab -e `编辑任务时间表文件

在最后一行添加：

`0 5,6,7 * * * cd /usr/local/src/Health-Data-Post && python3 HealthDataPost.py >> run.log`  

含义：每天5,6,7点整进入工作目录并且运行程序，将程序输出重定向至`run.log`文件中。

注：多次运行不会多次提交，程序会自动检测今日是否已经提交，未提交的才会提交。

## 收尾

保证服务器正常运行+正常联网

