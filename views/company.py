from flask import request, render_template, current_app, abort, redirect, url_for, flash
from flask_login import current_user

from forms import RegisterCompanyForm, CompanyDetailForm, company_required
from models.index import Company, Job, Delivery
from . import company_blu


@company_blu.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegisterCompanyForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录', 'success')
        return redirect(url_for('index.login'))

    return render_template("company/register.html", form=form, active='company_register')


@company_blu.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    flt = {Company.is_enable is True}
    if kw is not None and kw != '':
        # flt.update({Company.name.ilike('%{}%'.format(kw))})
        kw = '%{}%'.format(kw)
    # pagination = Company.query.filter(*flt).order_by(Company.updated_at.desc()).paginate(
    pagination = Company.query.filter(Company.is_enable==True, Company.name.like(kw)).order_by(Company.updated_at.desc()).paginate(
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



@company_blu.route('/account', methods=['GET', 'POST'])
@company_required
def edit():
    form = CompanyDetailForm(obj=current_user)
    logo_url = current_user.logo
    if form.validate_on_submit():
        logo_url = form.update_detail(current_user)
        print(logo_url)
        flash('企业信息更新成功', 'success')
    return render_template('company/edit.html', form=form, file_url=logo_url, panel='edit', active='manage')


@company_blu.route('/jobs')
@company_required
def jobs():
    page = request.args.get('page', default=1, type=int)
    pagination = current_user.jobs.order_by(Job.updated_at.desc()).paginate(
        page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
    return render_template('company/jobs.html', pagination=pagination, active='manage', panel='jobs')



@company_blu.route('/resumes')
@company_required
def resumes():
    status = request.args.get('status', '1')
    page = request.args.get('page', default=1, type=int)
    pagination = current_user.delivery.filter_by(status=status).order_by(Delivery.updated_at.desc()).paginate(
        page=page, per_page=current_app.config['LIST_PER_PAGE'], error_out=False)
    return render_template('company/resumes.html', pagination=pagination,
                           active='manage', panel='resumes', status=status)





@company_blu.route('/resume/accept')
@company_required
def resume_accept():
    delivery_id = request.args.get('delivery_id')
    delivery = current_user.delivery.filter_by(id=delivery_id).first_or_404()
    delivery.accept()
    db.session.add(delivery)
    db.session.commit()
    flash('已列入面试', 'success')
    return redirect(url_for('company.resumes'))


@company_blu.route('/resume/reject')
@company_required
def resume_reject():
    delivery_id = request.args.get('delivery_id')
    delivery = current_user.delivery.filter_by(id=delivery_id).first_or_404()
    delivery.reject()
    db.session.add(delivery)
    db.session.commit()
    flash('已列入不合适', 'warning')
    return redirect(url_for('company.resumes'))


@company_blu.errorhandler(413)
def page_not_found(error):
    flash('图片大小超过限制', 'warning')
    return redirect(request.path)
