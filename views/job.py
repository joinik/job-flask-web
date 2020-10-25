from flask import request, current_app, render_template, abort
from flask_login import current_user

from models.index import Job, EXP
from . import job_blu

@job_blu.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    flt = {Job.is_enable is True}
    if kw is not None and kw != '':
        flt.update({Job.name.like('%{}%'.format(kw))})
    pagination = Job.query.filter(*flt).order_by(
            Job.created_at.desc()).paginate(
                page=page,
                per_page=current_app.config['JOB_INDEX_PER_PAGE'],
                error_out=False
            )

    print ("------/ job---index---")

    return render_template('job/index.html', pagination=pagination,
                           kw=kw, filter=EXP, active='job')


@job_blu.route("/detail/<int:job_id>")
def detail(job_id):
    print("------detail---job")
    print(job_id)
    job_obj = Job.query.get_or_404 (job_id)
    if not job_obj.is_enable and job_obj.company_id != current_user.id:
        abort (404)
    return render_template ('job/detail.html', job=job_obj)
