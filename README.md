### 声明此项目， fork于 yifanzheng.github.io
### 但是 完全 是本人 自己从头到尾，重新写的一份，
# 简单的招聘网站demo
基于 Flask / Jinja2 / Bootstrap / MySQL 开发，仿照拉勾网的风格，实现了招聘网站的必需功能


## 环境
* Python 3
* MySQL
* redis

## 实现功能
* 个人和企业两种角色的注册登录编辑
* 职位和企业的索引页、详情页及搜索功能
* 个人简历上传和投递操作
* 企业对职位的增删改查上下线，及对简历的反馈处理

| 日期 | 计划 | 完成情况|
|---|---|---|
|2020-10-19|项目的大体设计，数据库的设计，|✔|
|2020-10-20|进行页面展示，用户登录注册，退出，功能||
|2020-10-21|进行详情页展示，功能||

## 项目流程
### 1. 第一天
项目的大体设计，数据库的设计
### 2. 第二天
进行页面展示，。。。。


## TODO
- [ ] 职位和企业的条件筛选
- [ ] 管理员后台和权限功能
- [ ] 简历支持 PDF，并将 PDF 转图片在线浏览
- [ ] 职位和企业该为列表展示
- [ ] 个人对职位收藏



#### 1. 安装 Python 依赖
```sh
$ pip3 install -r requirements.txt
```

#### 2. 修改配置文件

根据自己情况，修改 `job_web/config.py`

主要是 `SQLALCHEMY_DATABASE_URI` 数据库的链接

#### 3. 创建数据库

根据上面配置中的库名，创建数据库

#### 4. 利用 flask-migrate 建表

命令行终端，先进入项目目录，然后依次执行下列命令：

```sh

$ python manage.py db init
$ python manage.py db migrate -m '注释'
$ python manage.py db upgrade
```



#### 5. 生成测试数据（可选）

可执行 [test_data.py](https://github.com/zkqiang/job-web-demo/blob/master/data/test_data.py) 生成一些随机数据





