from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, logout_user, login_user

from forms import LoginForm
from models.index import Company, Job, User
from . import index_blu


@index_blu.route ("/")
def index():
	company_all = Company.query.filter (Company.is_enable.is_ (True)).order_by (Company.updated_at.desc ())
	companies = []
	# 循环公司 list
	for c in company_all:
		# 判断 公司职位
		if c and c.enabled_jobs ().count () != 0:
			companies.append (c)
			if len (companies) == 8:
				break
	jobs = Job.query.group_by (Job.company_id).order_by (Job.updated_at.desc ()).limit (12)
	return render_template ('index.html', active='index', jobs=jobs, companies=companies)


@index_blu.route ("/search")
def search():
	search_type = request.args.get ('type')
	kw = request.args.get ('kw')
	if search_type == 'job':
		return redirect (url_for ('job.index', kw=kw))
	elif search_type == 'company':
		return redirect (url_for ('company.index', kw=kw))
	else:
		return redirect (url_for ('index.index'))


@index_blu.route ("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect (url_for ('index.index'))

	# 生成 form 对象
	form = LoginForm ()
	# 1.判断用户是否 提交表单
	if form.validate_on_submit ():
		user_data = User.query.filter (User.email==form.email.data).first ()
		# 1.1 判断 用户是否 存在
		if not user_data:
			user_data = Company.query.filter (Company.email == form.email.data).first ()
			if not user_data:
				flash ("登录信息有误， 请重新登录", 'danger')
				return redirect (url_for ('index.login'))

		# 1.2 判断 用户 password
		if not user_data.check_password (form.password.data):
			flash ('登录信息有误，请重新登录', 'danger')
			return redirect (url_for ('index.login'))
		# 1.2 判断 用户 是否可用
		if not user_data.is_enable:
			flash ('该用户不可用，请联系网站管理员', 'danger')
			return redirect (url_for ('index.login'))
		login_user (user_data, form.remember_me.data)
		flash ('登录成功', 'success')
		next_page = request.args.get ('next')
		return redirect (next_page or url_for ('index.index'))
	return render_template ('login.html', form=form, active='login')


@index_blu.route ('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	# 自动清除 session 信息
	logout_user ()
	flash ('您已经退出登录', 'success')
	return redirect (url_for ('index.index'))
