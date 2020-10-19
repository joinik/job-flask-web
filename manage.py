from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session




# 1. 创建App对象
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(front)

# app.register_blueprint(user)
# app.register_blueprint(admin)
# app.register_blueprint(company)
# app.register_blueprint(job)

# 加载配置信息
app.config.from_pyfile("config.ini")

# db初始化配置App
db.init_app(app)

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