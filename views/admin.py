from datetime import timedelta, datetime

from flask import render_template, request, current_app, jsonify
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


@admin_blu.route ('/companys_review_detail.html')
def companys_review_detail():
	company_id = request.args.get ('id')
	company = Company.query.filter (company_id == Company.id).first ()

	return render_template ('admin1/companys_review_detail.html', companys=company)


@admin_blu.route ('/companys_review_detail/<int:company_id>', methods=["POST"])
def save_companys_review_detail(company_id):
	company = db.session.query (Company).filter (Company.id == company_id).first ()

	if not company:
		return jsonify ({
			"errno": 4001,
			"errmsg": "为找到此公司"
		})

	action = request.json.get ('action')
	reason = request.json.get ('reason')

	if action == "accept":
		company.is_enable = 1

	else:
		company.is_enable = 0
	# company.reason = reason
	try:
		# 保存到数据库
		db.session.commit ()
		print ("修改成功------------")
	except Exception as e:
		db.session.rollback ()
		print ("请重新操作")

	# 返回对应信息
	return jsonify ({
		"errno": 0,
		"errmsg": "成功"
	})


@admin_blu.route ('/jobs_edit.html')
def jobs_edit():
	page = int (request.args.get ('page', 1))
	paginate = Job.query.order_by (-Job.created_at).paginate (page, 5, False)
	return render_template ('admin1/jobs_edit.html', paginate=paginate)


@admin_blu.route ("/jobs_edit_detail.html")
def jobs_edit_detail():
	job_id = request.args.get ("id")
	job = Job.query.filter (job_id == Job.id).first ()
	return render_template ('admin1/jobs_edit_detail.html', jobs=job)


@admin_blu.route ('/jobs_edit_detail/<int:job_id>', methods=["POST"])
def save_jobs_edit_detail(job_id):
	job = Job.query.filter (job_id == Job.id).first ()

	if not job:
		return jsonify ({
			"errno": 5001,
			"errmsg": "未找到对应的job"
		})

	job.name = request.form.get ("title")
	job.description = request.form.get ("digest")
	job.treatment = request.form.get ("content")

	try:
		db.session.commit ()
	except Exception as e:
		db.session.rollback ()
		print ('修改 失败')

	return jsonify ({
		"errno": 0,
		"errmsg": "成功"
	})


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
