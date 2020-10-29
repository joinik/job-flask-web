from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_moment import Moment
from flask_script import Manager
from flask_session import Session
from flask_share import Share
from flask_uploads import UploadSet, IMAGES, configure_uploads
from utils.common import show_companys_status_name, show_company_website
from models import db


from models.index import User, Company
from views import admin_blu, index_blu, job_blu, company_blu, user_blu


# 配置 上传 属性
uploaded_resume = UploadSet('resume', IMAGES)
uploaded_logo = UploadSet('logo', IMAGES)

def register_blueprints(app):
	# 注册蓝图
	app.register_blueprint (admin_blu, url_prefix="/admin")
	app.register_blueprint (index_blu)
	app.register_blueprint (job_blu, url_prefix='/job')
	app.register_blueprint (company_blu, url_prefix='/company')
	app.register_blueprint (user_blu, url_prefix='/user')




def create_app():
	# 1. 创建App对象
	app = Flask (__name__)
	# 加载配置信息
	app.config.from_pyfile ("config.ini")

	# db初始化配置App
	db.init_app (app)

	# Session 对象， 存储到redis 中
	# Session(app)

	# 添加csrf 保护
	CKEditor (app)
	# 添加时间
	Moment (app)

	# loginManager() 登录 对象
	login_manager = LoginManager ()
	login_manager.init_app (app)
	configure_uploads(app, uploaded_resume)
	configure_uploads(app, uploaded_logo)


	@login_manager.user_loader
	def user_loader(id):
		if User.query.get (id):
			return User.query.get (id)
		elif Company.query.get (id):
			return Company.query.get (id)

	app.add_template_filter(show_companys_status_name)
	app.add_template_filter(show_company_website)
	login_manager.login_view = 'index.login'

	# 基于jinja2模板创建社交共享组件
	share = Share ()
	share.init_app (app)

	# 注册蓝图
	register_blueprints(app)


	# 添加数据库迁移工具
	manager = Manager (app)
	# 生成 migrate 对象，用来迁移数据库
	migrate = Migrate (app, db)
	# 添加db 命令
	manager.add_command ('db', MigrateCommand)

	return manager



if __name__ == '__main__':
	manager = create_app()
	manager.run ()
