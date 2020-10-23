import time

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError

from models import db
from models.index import User, Company

FINANCE_STAGE = ['未融资', '天使轮', 'A轮', 'B轮', 'C轮', 'D轮及以上', '上市公司', '不需要融资']
FIELD = ['移动互联网', '电子商务', '金融', '企业服务', '教育', '文化娱乐', '游戏', 'O2O', '硬件']
EXP = ['不限', '1年', '1-3年', '3-5年', '5-10年', '10年以上']
EDUCATION = ['不限学历', '专科', '本科', '硕士', '博士']
DEFAULT_LOGO = 'https://www.zhipin.com/v2/chat_v2/images/v2/defaultlogov2.jpg'


class RegisterUserForm (FlaskForm):
	""" 用户注册表单 """
	email = StringField ('邮箱', validators=[DataRequired (message='请填写内容'),
	                                       Email (message='请输入合法的email地址')],
	                     render_kw={'placeholder': '请输入email 地址'})

	phone = StringField ('手机号码', validators=[DataRequired (message='请填写手机号码'),
	                                         Length (11, 11), Regexp ('^1[35789]\d{9}', 0, '手机号码不合法')],
	                     render_kw={'placeholder': '输入手机号'})

	password = PasswordField ('密码', validators=[DataRequired (message='请填写密码'),
	                                            Length (6, 24, message='须在6～24个字符之间'),
	                                            Regexp (r'^[a-zA-Z]+\w+', message='仅限使用英文、数字、下划线，并以英文开头')],
	                          render_kw={'placeholder': '输入密码'})

	# EqualTo 比较两个字段的值
	repeat_password = PasswordField ('重复密码', validators=[DataRequired (message='请填写密码'),
	                                                     EqualTo ('password', message='两次密码不一致')],
	                                 render_kw={'placeholder': '请再次输入密码'})

	name = StringField ('姓名', validators=[DataRequired (message='请填写内容'),
	                                      Length (2, 8, message='须在2～8个字符之间')],
	                    render_kw={'placeholder': '输入姓名'})
	submit = SubmitField ('提交')

	def validate_email(self, field):
		if User.query.filter_by (email=field.data).first () or \
				Company.query.filter_by (email=field.data).first ():
			raise ValidationError ('邮箱已被其他账号使用')

	def create_user(self):
		# 创建用户
		user = User ()
		user.name = self.name.data
		user.email = self.email.data
		user.password = self.password.data
		user.phone = self.phone.data
		user.id = int (time.time () * 100000000)
		db.session.add (user)
		db.session.commit ()
		return user


class RegisterCompanyForm (FlaskForm):
	"""公司注册 的表单"""

	email = StringField ('邮箱', validators=[DataRequired (message='请填写内容'),
	                                       Email (message='请输入合法的Email地址')],
	                     render_kw={'placeholder': '请输入email'})


	password = PasswordField ('密码', validators=[DataRequired (message='请填写密码'),
	                                            Length (6, 24, message='须在6～24个字符之间'),
	                                            Regexp (r'^[a-zA-Z]+\w+', message='仅限使用英文、数字、下划线，并以英文开头')],
	                          render_kw={'placeholder': '请填写密码'})
	repeat_password = PasswordField ('重复密码', validators=[DataRequired (message='请填写密码'),
	                                                     EqualTo ('password', message='两次密码不一致')],
	                                 render_kw={'placeholder': '请再次填写密码'})

	phone = StringField ('手机号码', validators=[DataRequired (message='请填写手机号码'),
	                                         Length (11, 11), Regexp ('^1[35789]\d{9}', 0, '手机号码不合法')],
	                     render_kw={'placeholder': '输入手机号'})

	name = StringField ('企业名称', validators=[DataRequired (message='请填写内容'),
	                                        Length (2, 32, message='须在2～32个字符之间')],
	                    render_kw={'placeholder': '请输入企业姓名'})
	finance_stage = SelectField ('融资阶段', choices=[(i, i) for i in FINANCE_STAGE])
	field = SelectField ('行业领域', choices=[(i, i) for i in FIELD])
	description = StringField ('公司简介', validators=[Length (0, 50, message='最多50个字符')],
	                           render_kw={'placeholder': '请输入公司简介'})
	submit = SubmitField ('提交')


	def validate_email(self, field):
		if User.query.filter_by (email=field.data).first () or \
				Company.query.filter_by (email=field.data).first ():
			raise ValidationError ('邮箱已被其他账号使用')


	def create_company(self):
		company = Company ()
		company.name = self.name.data
		company.email = self.email.data
		company.password = self.password.data
		db.session.add (company)
		db.session.commit ()
		return company


class LoginForm (FlaskForm):
	"""登录表单"""
	email = StringField ('邮箱', validators=[DataRequired (message='请填写内容'),
	                                       Email (message="请输入合法的email地址")],
	                     render_kw={'placeholder': '输入email'})

	password = PasswordField ('密码', validators=[DataRequired (message='请填写密码'),
	                                            Length (6, 24, message="需在6-24个字符之间")],
	                          render_kw={'placeholder': '输入密码'})

	remember_me = BooleanField ('记住登录状态')
	submit = SubmitField ('登录')
