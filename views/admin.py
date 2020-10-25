from flask import render_template, request, current_app

from forms import admin_required
from models.index import Company, User, Job
from . import admin_blu
import test_data


@admin_blu.route ("/")
def index():
	return render_template ("admin/index.html")


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
