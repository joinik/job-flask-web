
from flask import render_template

from . import admin_blu
import test_data

@admin_blu.route("/")
def index():
	# test_data.run()
	return render_template("admin/index.html")