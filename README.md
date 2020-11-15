## 项目是干什么的？

自动完成山东水利职业学院“智慧山水”平台的**每日健康上报**。

免去手动操作。

## 注意事项

程序只会提交提前设定好的身体健康数据，所以若身体情况发送变动必须及时更新数据，否则学校将会收到错误信息，防疫工作也会受到影响。

## 如何下载代码？

`git clone git@github.com:imldy/health-data-post.git`

或者

[点我下载](https://github.com/imldy/health-data-post/archive/master.zip)

## 各个文件作用说明

1. doc/——说明文档/教程

2. **HealthDataPost.py——主程序**

3. README.md——项目相关信息

4. **students_data.json——主程序需要的配置文件**

其中**2、4**为程序运行的**必须项**。

## 如何做到自动上报？

### 1、先设置自己的账号、密码、健康信息

**用户信息说明：[students_data_explain.md](./doc/students_data_explain.md)**

### 2、设置定时启动

**定时启动说明：[Regular_operation.md](./doc/Regular_operation.md)**

## 如何修改并在本地运行代码？

注意！如果你仅仅是想自动上报，完全不需要修改代码，也不需要做这一步，这一步是为软件开发准备的。

以下是我所使用的软件/库版本，其他版本请自行测试。

请安装：![Python](https://img.shields.io/badge/Python-3.8.2-blue.svg)![PiP](https://img.shields.io/badge/pip-20.0.2-5e7c85.svg)![lxml](https://img.shields.io/badge/lxml-4.5.0-Lime.svg)![Requests](https://img.shields.io/badge/requests-2.23.0-yellowgreen.svg)![urllib3](https://img.shields.io/badge/urllib3-1.25.8-Tomato.svg)

## 免责声明

本程序仅供交流使用，使用者使用此程序造成的任何后果由使用者自行承担。

## 如果有帮助到你请点一下★Star

![点★Star](https://qiniu-blog.taokeml.top/PicGo/20200920184106.png-ldy.blog)
