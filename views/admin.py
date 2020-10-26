
from datetime import timedelta, datetime

from flask import render_template, request, current_app
from flask_login import current_user
from sqlalchemy import extract

from forms import admin_required
from models import db
from models.index import Company, User, Job
from . import admin_blu
import test_data


@admin_blu.route ("/")
def index():
	user = current_user
	return render_template ("admin1/index.html", user=user)

@admin_blu.route ("/user_list.html")
def user_list():
	page = int (request.args.get ("page", 1))

	# 查询用户数据 列表
	pag_users = db.session.query (User).paginate (page, 3, False)

	if pag_users:
		pass
	return render_template ("admin1/user_list.html", pages=pag_users)



@admin_blu.route ("/companys_review.html")
def companys_review():
	page = int (request.args.get ("page", 1))
	paginate = db.session.query (Company).order_by (-Company.created_at).paginate (page, 5, False)
	return render_template ("admin1/companys_review.html", paginate=paginate)




@admin_blu.route('/companys_review_detail.html')
def companys_review_detail():
	job_id = request.args.get("id", 0)

	job = db.session.query(Job).filter(Job.company_id == job_id).first()
	return render_template('admin1/companys_review_detail.html', jobs=job)








@admin_blu.route ('/user')
@admin_required
def user():
	page = request.args.get ('page', default=1, type=int)
	pagination = User.query.paginate (
		page=page,
		per_page=current_app.config['LIST_PER_PAGE'],
		error_out=False
	)
	return render_template ('admin/user.html', pagination=pagination)


@admin_blu.route ('/company')
@admin_required
def company():
	page = request.args.get ('page', default=1, type=int)
	pagination = Company.query.paginate (
		page=page,
		per_page=current_app.config['LIST_PER_PAGE'],
		error_out=False
	)
	return render_template ('admin/company.html', pagination=pagination)


@admin_blu.route ('/job')
@admin_required
def job():
	page = request.args.get ('page', default=1, type=int)
	pagination = Job.query.paginate (
		page=page,
		per_page=current_app.config['LIST_PER_PAGE'],
		error_out=False
	)
	return render_template ('admin/job.html', pagination=pagination)
