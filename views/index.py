from flask import render_template, redirect, url_for, request

from models.index import Company, Job
from . import index_blu

@index_blu.route("/")
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
	jobs = Job.query.group_by(Job.company_id).order_by(Job.updated_at.desc()).limit(12)
	return render_template ('index.html', active='index', jobs=jobs, companies=companies)

@index_blu.route("/search")
def search():
	search_type = request.args.get ('type')
	kw = request.args.get ('kw')
	if search_type == 'job':
		return redirect (url_for ('job.index', kw=kw))
	elif search_type == 'company':
		return redirect (url_for ('company.index', kw=kw))
	else:
		return redirect (url_for ('index.index'))



@index_blu.route("/login")
def login():
	return render_template("login.html")