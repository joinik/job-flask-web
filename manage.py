from flask import Flask
from flask_ckeditor import CKEditor
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment
from flask_script import Manager
from flask_session import Session
from models import db

# 1. 创建App对象
from views import admin_blu, index_blu, job_blu, company_blu

app = Flask (__name__)

# 注册蓝图
app.register_blueprint(admin_blu, url_prefix="/admin")
app.register_blueprint (index_blu)
app.register_blueprint(job_blu, url_prefix='/job')
app.register_blueprint(company_blu, url_prefix='/company')


# app.register_blueprint(user)
# app.register_blueprint(company)
# app.register_blueprint(job)

# 加载配置信息
app.config.from_pyfile ("config.ini")

# db初始化配置App
db.init_app (app)

CKEditor(app)
Moment(app)

# Session 对象， 存储到redis 中
# Session(app)

# 添加数据库迁移工具
manager = Manager (app)
# 生成 migrate 对象，用来迁移数据库
migrate = Migrate (app, db)
# 添加db 命令
manager.add_command ('db', MigrateCommand)

if __name__ == '__main__':
	manager.run ()
