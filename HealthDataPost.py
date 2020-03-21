# time：2020年3月18日17:46:37
# 无变化直接执行即可，身体情况有变化需更改源码
from urllib import parse
from lxml import etree
import requests
import time
import json


class Student(object):
    ID = ""
    password = ""
    health_data_dict = {}

    @classmethod
    def dataPost(cls):
        # 设置登录时所要的数据（账号——即学号和密码）
        WebSite.login_data["username"] = cls.ID
        WebSite.login_data["password"] = cls.password

        # 保持访问连接
        session = requests.session()
        # 登录
        res0 = session.post(url=WebSite.login_api, data=WebSite.login_data, headers=WebSite.login_headers)
        if res0.status_code == 200:
            # 登录成功
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 登录成功")
            time.sleep(0.5)

            # 设置表单页面的url和请求头中的Referer
            WebSite.form_web_url = WebSite.form_web_url_head + cls.ID
            WebSite.form_web_headers["Referer"] = WebSite.form_web_url
            # 请求表单所在的网页
            res1 = session.get(url=WebSite.form_web_url, headers=WebSite.form_web_headers).content.decode("UTF-8")
            html1 = etree.HTML(res1)

            # 这里的代码用于更新表单，正常每天首次提交用不到这些代码
            try:
                id = html1.xpath("//input[@name='did']/@value")[0]
            except IndexError:
                cls.health_data_dict["id"] = ""
            else:
                cls.health_data_dict["id"] = id
            try:
                prompt_info = html1.xpath("//div[@class='tb_txt']/text()")[0]
            except IndexError:
                # 如果没找到提示今天已经上报的信息而报错了，就初步判断今天还没上报
                if ("您已上报" in res1) and ("健康信息，无需再次提报" in res1):
                    # 如果固定位置没找到提示信息，但是网页其他地方找到了
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 警告：网站发生变化，推荐手动确认网页情况，以免发生错误")
                else:
                    # 如果固定位置没找到提示信息，且网页源码都未发现相关提示
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 判断为还未提报今日身体信息")
                    time.sleep(3)
                    # 提交
                    # 直接提交汉字可能会出错，URL编码处理
                    WebSite.submit_api_url_and_data = WebSite.submit_api_url + parse.urlencode(cls.health_data_dict)
                    # 设置提交数据api的请求头中的Referer
                    WebSite.submit_api_headers["Referer"] = WebSite.form_web_url

                    res = session.get(url=WebSite.submit_api_url_and_data, headers=WebSite.submit_api_headers)
                    # 通过返回结果判断本次是否提交成功
                    if "OK" in res.text and res.status_code == 200:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 本次提报成功")
                        time.sleep(5)
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - " + "提报结束")
                    else:
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - 错误：本次提报失败，详情查看：" + res.text)
                        time.sleep(5)
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - " + "提报结束")
            else:
                # 没报错就代表以及提交了
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - " + prompt_info)
                time.sleep(5)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " - " + "提报结束")
        else:
            print("登录出现异常")


class WebSite(object):
    # 登录账户所用的数据
    login_api = "http://sso.sdwcvc.cn/index.php?rid=verifyWebUser"
    login_data = {}
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    }

    # 请求表单页面所要的数据
    form_web_url_head = "http://pubinfo.sdwcvc.cn/Xxtb/dailyRecord?userid="
    form_web_url = ""
    form_web_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Cookie": Cookie,
        "Host": "pubinfo.sdwcvc.cn",
        "Referer": "",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    }
    # 提交健康情况所要的数据
    submit_api_url = "http://pubinfo.sdwcvc.cn/Xxtb/saveRecord?"
    submit_api_url_and_data = ""
    submit_api_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        # "Cookie": Cookie,
        "Host": "pubinfo.sdwcvc.cn",
        "Referer": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }


# ！！！！------------改成自己的学号和密码------------！！！！
# ！！！！-------外部健康文件要改成自己的，注意要填网页上有的选项的值，除了第9可以随便填，其他都是固定格式-------！！！！
# 加载外部健康文件
health_file = open("students_data.json", "r", encoding="utf-8")
# 编码为python对象
students = json.loads(health_file.read())

len_students = len(students)
# print(len_students)
# 循环其列表中所有的学生
for student in students:
    print("正在进行第{}/{}个用户".format(students.index(student) + 1, len_students))
    Student.ID = student["stu_id"]
    Student.password = student["password"]
    Student.health_data_dict = student["health_data_dict"]
    Student.dataPost()
    time.sleep(5)