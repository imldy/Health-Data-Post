## 项目是干什么的？

自动完成山东水利职业学院“智慧山水”平台的**每日健康上报**。

免去手动操作。

## 注意事项

程序只会提交提前设定好的身体健康数据，所以若身体情况发送变动必须及时更新数据，否则学校将会收到错误信息，防疫工作也会受到影响。

## 各个文件作用说明

1. doc/——说明文档/教程

2. **HealthDataPost.py——主程序**

3. README.md——项目相关信息

4. **students_data.json——主程序需要的配置文件**

其中**2、4**为程序运行的**必须项**。

## 如何做到自动上报？

### 1. 读懂配置文件

[配置文件说明](./doc/students_data_explain.md)

### 2.部署程序

#### 1. 我有/我想用自己的电脑/服务器/VPS来自动上报

1. [Windows 系统](./doc/Post_Windows.md)
2. [Linux 系统](./doc/Post_Linux.md)

#### 2. 我没有/我不想用自己的电脑/服务器/VPS来自动上报

1. [使用腾讯云云函数功能](./doc/Post_TencentCloud.md)
2. [使用 GitHub Actions 功能](./doc/Post_GitHubActions.md) （暂未实现）

## 免责声明

本程序仅供交流使用，使用者使用此程序造成的任何后果由使用者自行承担。

## 如果有帮助到你请点一下★Star

![点★Star](https://qiniu-blog.taokeml.top/PicGo/20200920184106.png-ldy.blog)
