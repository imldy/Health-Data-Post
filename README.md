

## 与主分支区别

主分支中是使用python脚本进行批量上报，而此分支为GUI版本

并且图标相关代码没用使用异常捕获，请保证ico文件与exe文件在同一路径下。

* **仅支持Windows系统的提交上报**
* **支持多人员**
* **目前暂不支持批量上报**
* **经纬度信息不可修改，地址为山东水利职业学院。**

## 文件作用说明

1. **photos.ico**:图标文件

2. **Users.json**: 主程序所需配置文件

   {
   "name":姓名,
   "stu_id":智慧山水学号,
   "password":智慧山水密码
   },

   前两项未结束时需要逗号,最后一项无需逗号
   在最后的括号外部( } )如果是本文件的最后一项无需逗号( } )
   非最后一项需要逗号( }, )

3. **上报工具.exe**:主程序

## 如何修改上报信息

**在`students_data.json`内，应该按照如下规则进行修改。**

最外层的`[]`内存放所有学生的所有信息。其中每个元素为一个学生的信息。

每个学生信息由字典组成，即“学生信息字典”，每个字典中含有学号、密码、姓名。

#### 学生信息字典释义

##### 外层每个key的释义

| key      | 是否必改 | 释义                                       |
| -------- | ---- | ---------------------------------------- |
| stu_id   | 是    | 学生登录智慧山水平台http://sso.sdwcvc.cn/ 或者“智慧山水”APP的的账号，即学号 |
| password | 是    | 登录密码                                     |
| name     | 是    | 在GUI中显示的字段，一般填写学生姓名                      |



