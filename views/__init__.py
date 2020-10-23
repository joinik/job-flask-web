
from flask import Blueprint

admin_blu = Blueprint("admin", __name__)
index_blu = Blueprint("index", __name__)
job_blu = Blueprint("job", __name__)
company_blu = Blueprint("company", __name__)
user_blu = Blueprint("user", __name__)


from . import admin
from . import index
from . import job
from . import company
from . import user