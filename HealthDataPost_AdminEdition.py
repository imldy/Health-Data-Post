from urllib import parse
from lxml import etree
import requests
import time
import json
import tkinter as tk
from tkinter import ttk, scrolledtext  # 导入ttk模块，因为下拉菜单控件在ttk中


def getNowTime():
    """
    获取当前已格式化的时间，格式：****-**-** **:**:**
    :return: 返回格式化后的当前时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Student(object):
    health_data_dict = {"id": "", "filldate": "", "mqjk": "健康", "jrjk": "健康", "city1": "山东省", "city2": "日照市",
                        "city3": "东港区", "sfwc": "0", "sfjc": "0", "sfhb": "否", "zb": "不清楚", "jchz": "否",
                        "other": "37.2度及以下", "other1": "秦楼街道聊城路山东水利职业学院", "other2": "否", "other3": "37.2度及以下",
                        "other4": "37.2度及以下", "other5": "", "other6": "否", "other7": "119.554555,35.455762）"}

    def __init__(self, ID, password, health_data_dict):
        self.ID = ID
        self.password = password
        self.health_data_dict = health_data_dict
        # 保持访问连接
        self.session = requests.session()

    def login(self):
        """
        登录
        :return: 返回登录的响应信息
        """
        # 设置登录时所要的数据（账号——即学号和密码）
        WebSite.login_data["username"] = self.ID
        WebSite.login_data["password"] = self.password

        # 登录
        res0 = self.session.post(url=WebSite.login_api, data=WebSite.login_data, headers=WebSite.login_headers)
        return res0

    def submit(self):
        """
        执行提交信息的动作
        :return:
        """
        # 提交
        # 直接提交汉字可能会出错，URL编码处理
        WebSite.submit_api_url_and_data = WebSite.submit_api_url + parse.urlencode(
            self.health_data_dict)
        # 设置提交数据api的请求头中的Referer
        WebSite.submit_api_headers["Referer"] = WebSite.form_web_url

        res = self.session.get(url=WebSite.submit_api_url_and_data, headers=WebSite.submit_api_headers)
        return res

    def dataPost(self, Information_Window):
        # 调用login方法进行登录
        res0 = self.login()
        if res0.status_code == 200:
            # 登录成功
            gui_insert(Information_Window, getNowTime() + " - 登录成功")
            time.sleep(0.5)
            # 设置表单页面的url和请求头中的Referer
            # 无需设置url，直接访问即可
            # WebSite.form_web_url = WebSite.form_web_url_head + cls.ID
            WebSite.form_web_headers["Referer"] = WebSite.form_web_url
            # 请求表单所在的网页
            res1 = self.session.get(url=WebSite.form_web_url, headers=WebSite.form_web_headers).content.decode("UTF-8")
            html1 = etree.HTML(res1)

            # 这里的代码用于更新表单，正常每天首次提交用不到这些代码
            # try:
            #     id = html1.xpath("//input[@name='did']/@value")[0]
            # except IndexError:
            #     cls.health_data_dict["id"] = ""
            # else:
            #     cls.health_data_dict["id"] = id

            try:
                # 查找提示信息
                # 提取提示信息
                prompt_info = html1.xpath("//div[@class='title']/text()")[0]
            except IndexError:
                # 如果没找到提示今天已经上报的信息而报错了，就初步判断今天还没上报
                gui_insert(Information_Window, "未找到是否上报的提示信息")
            else:
                # 没报错就代表提取到是否上报的提示信息了
                # 去除提示信息前后的空格
                prompt_info = prompt_info.strip()
                # 根据提示信息判断是否提交
                if "您已上报" not in prompt_info:
                    # 固定位置未找到已提交的提示信息
                    if ("您已上报" in res1) and ("健康信息" in res1):
                        # 如果固定位置没找到提示信息，但是网页其他地方找到了
                        gui_insert(Information_Window, getNowTime() + " - 警告：网站发生变化，推荐手动确认网页情况，以免发生错误")
                    else:
                        # 如果固定位置没找到提示信息，且网页源码都未发现相关提示
                        gui_insert(Information_Window, getNowTime() + " - 判断为还未提报今日身体信息")
                        time.sleep(1)
                        # 提交的准备工作，设置当前日期。
                        self.health_data_dict["fillDate"] = html1.xpath('/html//input[@name="ddate"]/@value')
                        # 提交动作
                        res = self.submit()
                        # 通过返回结果判断本次是否提交成功
                        if "OK" in res.text and res.status_code == 200:
                            gui_insert(Information_Window, getNowTime() + " - 本次提报成功，返回结果：" + res.text)
                        else:
                            gui_insert(Information_Window, getNowTime() + " - 错误：本次提报失败，详情查看：" + res.text)
                else:
                    # 判断为已提交
                    gui_insert(Information_Window, getNowTime() + " - " + prompt_info)
                    time.sleep(1)
                    gui_insert(Information_Window, getNowTime() + " - " + "提报结束")
        else:
            gui_insert(Information_Window, "登录出现异常")


class WebSite(object):
    # 登录账户所用的数据
    login_api = "http://sso.sdwcvc.cn/index.php?rid=verifyWebUser"
    login_data = {}
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    }

    # 请求表单页面所要的数据
    # form_web_url_head =
    form_web_url = "http://pubinfo.sdwcvc.cn/xxtb2/dailyRecord"
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
    submit_api_url = "http://pubinfo.sdwcvc.cn/xxtb2/saveRecord?"
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


class MyGui():
    def __init__(self, root_window):
        self.root_window = root_window

    def report(self):
        health_file = open("Users.json", "r", encoding="utf-8")
        # 编码为python对象
        students = json.loads(health_file.read())
        CURRENT = self.cmb.current()
        try:
            self.Information_Window.insert("end", "正在进行" + students[CURRENT]["name"] + '\n')
            stu = Student(students[CURRENT]["stu_id"], students[CURRENT]["password"], Student.health_data_dict)
            stu.dataPost(self.Information_Window)
            gui_insert(self.Information_Window, "=======结束========")
        except:
            self.Information_Window.insert("end", "您还未选择人员" + '\n')
            gui_insert(self.Information_Window, "=======结束========")

    # 设置窗口
    def set_init_window(self):
        self.root_window.title("上报工具Ver.Bata")  # 窗口名
        self.root_window.geometry('800x500+10+10')
        self.root_window.iconbitmap(default="photos.ico")
        # 输出窗口
        self.Information = tk.LabelFrame(self.root_window, text="操作信息", padx=10, pady=10)  # 创建子容器，水平，垂直方向上的边距均为10
        self.Information.place(x=20, y=20)
        self.Information_Window = scrolledtext.ScrolledText(self.Information, width=70, height=20, padx=10, pady=10,wrap=tk.WORD)
        self.Information_Window.grid()
        # 按钮
        self.button_post = tk.Button(self.root_window, text="提交", command=self.report)
        self.button = tk.Button(self.root_window, text="关闭", command=self.root_window.quit)
        self.button.place(x=400, y=460)
        self.button_post.place(x=350, y=460)
        # 下拉框
        self.cmb = ttk.Combobox(self.root_window)
        # 处理数据源
        health_file = open("Users.json", "r", encoding="utf-8")
        # 编码为python对象
        students = json.loads(health_file.read())
        student_name = []
        for student in students:
            student_name.append(student["name"])
        self.cmb['value'] = student_name
        self.cmb.place(x=600, y=160)


def gui_start():
    init_window = tk.Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MyGui(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()


def gui_insert(Information_Window, Str):
    Information_Window.insert("end", Str + "\n")


if __name__ == '__main__':
    gui_start()





