from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
@admin_required
def index():
    return redirect(url_for('topic.index'))


@main.route("/add", methods=["POST"])
@admin_required
def add():
    form = request.form
    u = current_user()
    m = Board.new(form)
    return redirect(url_for('topic.index'))

