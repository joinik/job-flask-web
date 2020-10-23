from flask import url_for, flash, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from forms import RegisterUserForm
from . import user_blu


@user_blu.route("/register", methods=["POST","GET"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index.index'))

	form = RegisterUserForm()
	if form.validate_on_submit():
		form.create_user()
		flash('注册成功， 请登录', 'success')
		return redirect(url_for('index.index'))
	return render_template('user/register.html', form=form, active='user_register')

