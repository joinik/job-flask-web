from flask import url_for, flash, render_template, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from forms import RegisterUserForm, UserResumeForm, UserDetailForm
from models.index import Delivery
from . import user_blu


@user_blu.route ("/register", methods=["POST", "GET"])
def register():
	if current_user.is_authenticated:
		return redirect (url_for ('index.index'))

	form = RegisterUserForm ()
	if form.validate_on_submit ():
		form.create_user ()
		flash ('注册成功， 请登录', 'success')
		return redirect (url_for ('index.index'))
	return render_template ('user/register.html', form=form, active='user_register')


@user_blu.route ('/resume', methods=['POST', 'GET'])
def resume():
	'''信息管理'''
	if not current_user.is_user ():
		return redirect (url_for ('index.index'))

	form = UserResumeForm ()
	resume_url = current_user.resume
	if form.validate_on_submit ():
		resume_url = form.upload_resume (current_user)
	return render_template ('user/resume.html', form=form, file_url=resume_url, active='manage', panel='resume')


@user_blu.route ('/delivery', methods=['POST', 'GET'])
@login_required
def delivery():
	'''交易'''
	if not current_user.is_user ():
		return redirect (url_for ('index.index'))

	status = request.args.get ('status', None)
	page = request.args.get ('page', default=1, type=int)
	if status:
		pagination = current_user.delivery.filter_by (status=status).order_by (Delivery.updated_at.desc ()).paginate (
			page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
	else:
		pagination = current_user.delivery.order_by (Delivery.updated_at.desc ()).paginate (
			page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
	return render_template ('user/delivery.html', pagination=pagination,
	                        active='manage', panel='delivery', status=status)


@user_blu.route ('/account', methods=['GET', 'POST'])
@login_required
def edit():
	if not current_user.is_user ():
		return redirect (url_for ("front.index"))
	form = UserDetailForm (obj=current_user)
	if form.validate_on_submit ():
		form.update_detail (current_user)
		flash ('个人信息更新成功', 'success')
		return redirect (url_for ('user.edit'))
	return render_template ('user/edit.html', form=form, active='manage', panel='edit')


@user_blu.errorhandler (413)
def page_not_found(error):
	flash ('文件大小超过限制', 'warning')
	return redirect (request.path)
