from flask import request, render_template, current_app

from models.index import Company, Job
from . import company_blu

@company_blu.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    flt = {Company.is_enable is True}
    if kw is not None and kw != '':
        flt.update({Company.name.ilike('%{}%'.format(kw))})
    pagination = Company.query.filter(*flt).order_by(Company.updated_at.desc()).paginate(
        page=page, per_page=current_app.config['COMPANY_INDEX_PER_PAGE'], error_out=False)
    return render_template('company/index.html', pagination=pagination, kw=kw, active='company')



@company_blu.route('/<int:company_id>')
def detail(company_id):
    company_obj = Company.query.get_or_404(company_id)
    if not company_obj.is_enable:
        abort(404)
    if request.args.get('job'):
        page = request.args.get('page', default=1, type=int)
        pagination = company_obj.enabled_jobs().order_by(Job.updated_at.desc()).paginate(
            page=page, per_page=current_app.config['COMPANY_DETAIL_PER_PAGE'], error_out=False)
        return render_template('company/detail.html', pagination=pagination, panel='jobs', company=company_obj)
    return render_template('company/detail.html', company=company_obj, panel='about', active='detail')
