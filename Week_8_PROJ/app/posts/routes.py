from flask import Blueprint

bp = Blueprint('posts', __name__)

@bp.route('/new')
def new_post():
    return "Create New Post"
