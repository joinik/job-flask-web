from flask import request, current_app, render_template, abort, flash, redirect, url_for
from flask_login import current_user, login_required

from models import db
from models.index import Job, EXP, Delivery
from . import job_blu


@job_blu.route ('/')
def index():
	page = request.args.get ('page', default=1, type=int)
	kw = request.args.get ('kw')
	flt = {Job.is_enable is True}
	if kw is not None and kw != '':
		flt.update ({Job.name.like ('%{}%'.format (kw))})
	pagination = Job.query.filter (*flt).order_by (
		Job.created_at.desc ()).paginate (
		page=page,
		per_page=current_app.config['JOB_INDEX_PER_PAGE'],
		error_out=False
	)
	if not pagination:

		return redirect(url_for('index.index'))
	print ("------/ job---index---")

	return render_template ('job/index.html', pagination=pagination,
	                        kw=kw, filter=EXP, active='job')


@job_blu.route ("/detail/<int:job_id>")
def detail(job_id):
	print ("------detail---job")
	print (job_id)
	job_obj = Job.query.get_or_404 (job_id)
	if not job_obj.is_enable and job_obj.company_id != current_user.id:
		abort (404)
	return render_template ('job/detail.html', job=job_obj)


@job_blu.route ("/<int:job_id>/apply", methods=["GET", "POST"])
@login_required
def apply(job_id):
	'''发布简历'''
	job_obj = Job.query.get_or_404 (job_id)
	if not current_user.is_user ():
		abort (404)
	if not current_user.resume:
		flash ('请先上传简历', 'warning')
		return redirect (url_for ('user.resume'))
	elif job_obj.is_applied ():
		flash ('已经投递过该职位', 'warning')
		return redirect (url_for ('job.detail', job_id=job_id))
	delivery = Delivery (
		job_id=job_id,
		user_id=current_user.id,
		company_id=job_obj.company_id,
		resume=current_user.resume
	)
	db.session.add(delivery)
	db.session.commit()
	flash('简历投递成功', 'success')
	return redirect(url_for('job.detail', job_id=job_id))



